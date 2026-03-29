#draft_codes.txt
from pymongo import MongoClient
import os
from flask_mail import Mail, Message


# MongoDb setup 
MONGO_URI = os.environ.get("MONGO_URI", "mongodb://localhost:27017/my_database")

client = MongoClient(MONGO_URI)
db = client['e_gallery_database']
photos_collection = db['photos']

# Flask Hundler 
import os
from flask import Flask, render_template,request,jsonify

app = Flask(__name__) 

# ImgFolder config
UPLOAD_FOLDER = "static/default_images"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER 

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
    print(f"Created folder: {UPLOAD_FOLDER}")

# Email handler 


app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465 
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True 
app.config['MAIL_USERNAME'] = 'auw242106@auw.edu.bd'
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD') # check this if email not working
app.config['MAIL_DEFAULT_SENDER'] = 'auw242106@auw.edu.bd'

mail = Mail(app)


@app.route("/") 
def main(): 
     return render_template("index.html")

@app.route("/edit_req")
def edit_req():
     return render_template("edit_req.html")


@app.route("/api/delete_request", methods=['POST'])
def delete_request():
     try:
          data = request.get_json()
          sender_name = data.get('sender')
          image_name = data.get('imageName')
          reason = data.get('reason')
          # Email for edit 
          msg = Message(
                    subject="Your photo fron E_visual gallery.",
                    recipients= ["auw242106@auw.edu.bd"]
                    )
               
               # The template loader 
          msg.html = render_template(
               "email_template.html", 
               sender_name=sender_name, 
               photo_description= f"Reason for deletion :{reason} ",
               email_reason = "Delete this image from dataBase.."
          )
          
          filepath = os.path.join(app.config["UPLOAD_FOLDER"], image_name)
          if os.path.exists(filepath):
               with open(filepath,"rb") as img :
                    msg.attach(image_name, "image/jpeg", img.read())
          else : 
               print(f"Warning: {image_name} not found in folder. Sending without image ")
          try:
               mail.send(msg)
               return jsonify({"message" : "Request sent successfully, it will take at most two working days to approve your reqest :)"}) , 200
          except Exception as e :
               print(f"Error : {e}")
               return jsonify({"message": "Failed to send email "}), 500
     except Exception as e:
        print(f"MAIL ERROR: {e}")
        #return JSON even if it fails
        return jsonify({"error": "Mail server connection timed out. Please try again later."}), 504



@app.route("/api/photos") 
def photo_render():
     # get all doc, _id hide
     photos = list(photos_collection.find({},{"_id":0}))
     return jsonify(photos) 


@app.route("/api/photos", methods=['POST'])
def photo_upload():
     file= request.files["file"]
     description = request.form["description"]
     sender = request.form["sender"]
     email = request.form.get("email")

     filename = file.filename
     filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
     file.save(filepath)

     # Gallery_data
     new_photo = {
          "filename": filename,
          "description" : description,
          "sender": sender
     }

     # Save to database
     photos_collection.insert_one(new_photo)
     
     if email:
          msg = Message(
                subject="Your photo fron E_visual gallery.",
               recipients=[email]
               )
              
          # The template loader 
          msg.html = render_template(
            "email_template.html", 
            sender_name=sender, 
            photo_description=description,
            email_reason = "We've successfully received your upload!"
        )
          with open(filepath,"rb") as img :
               msg.attach(filename, "image/jpeg", img.read())
          mail.send(msg) 
     
     return jsonify({ "message": "Done uploadeing "}), 201
    

@app.errorhandler(404)
def error_page(error):
     return render_template("404.html"), 404


if __name__ == "__main__":
    # running LOCALLY
    app.run(debug=True)
else:
    pass



# http://127.0.0.1:5000



