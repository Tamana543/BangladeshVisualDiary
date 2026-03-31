#draft_codes.txt
from pymongo import MongoClient
import os
from flask import Flask,render_template, request, jsonify




# MongoDb setup 
MONGO_URI = os.environ.get("MONGO_URI", "mongodb://localhost:27017/my_database")

client = MongoClient(MONGO_URI)
db = client['e_gallery_database']
photos_collection = db['photos']

# Flask Hundler 

app = Flask(__name__) 


# Email handler 



# ImgFolder config
UPLOAD_FOLDER = "static/default_images"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER 

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
    print(f"Created folder: {UPLOAD_FOLDER}")



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

          admin_email = os.environ.get('MAIL_USERNAME')

          if not admin_email : 
               return jsonify({"error": "Admin email have problem"}), 500
          
          # Email for edit 
          html_content = render_template(
              "email_template.html", 
            sender_name=sender_name, 
            photo_description=f"Reason for deletion: {reason}",
            email_reason=f"Delete this image from database: {image_name}" 
          )
          
          filepath = os.path.join(app.config["UPLOAD_FOLDER"], image_name)

          return jsonify({
            "message": "Request sent successfully, it will take at most two working days to approve your request :)"
        }), 200

     except Exception as del_e :
          print(f"Delete request error : {del_e}")
          return jsonify({"error":"Delete error, something went wrong"}), 500


@app.route("/api/photos") 
def photo_render():
     # get all doc, _id hide
     photos = list(photos_collection.find({},{"_id":0}))
     valid_photos = []
     for photo in photos:
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], photo['filename'])
        # Only show the photo if the file actually exists on the server
        if os.path.exists(filepath):
            valid_photos.append(photo)
            
     return jsonify(valid_photos) 


@app.route("/api/photos", methods=['POST'])
def photo_upload():
     try : 
          file= request.files["file"]
          description = request.form["description"]
          sender = request.form["sender"]
          email = request.form.get("email")

          filename = file.filename
          filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
          file.save(filepath)

          # save  to dataBase 
          new_photo = {
               "filename": filename,
               "description" : description,
               "sender": sender
          }
          photos_collection.insert_one(new_photo)
          
          if email:
              html_content = render_template(
                    "email_template.html", 
                    sender_name=sender, 
                    photo_description=description,
                    email_reason="We've successfully received your upload!"
               )
            
          return jsonify({"message" : "Photo uploaded successfully!"}), 201
     except Exception as phot_em_err :
          print(f"Upload Error: {phot_em_err}")
          return jsonify({"error":"Failed to upload photo"}), 500
    

@app.errorhandler(404)
def error_page(error):
     return render_template("404.html"), 404


if __name__ == "__main__":
    # running LOCALLY
    app.run(debug=True)
else:
    pass



# https://bangladeshvisualdiary.onrender.com



