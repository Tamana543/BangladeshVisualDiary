#draft_codes.txt
from pymongo import MongoClient
import os
import resend
import base64



# MongoDb setup 
MONGO_URI = os.environ.get("MONGO_URI", "mongodb://localhost:27017/my_database")

client = MongoClient(MONGO_URI)
db = client['e_gallery_database']
photos_collection = db['photos']

# Flask Hundler 
import os
from flask import Flask, render_template,request,jsonify

app = Flask(__name__) 


# Email handler 
resend.api_key = os.environ.get("RESEND_API_KEY")

def send_gallery_email(to_email, subject, html_content, attachment_path=None, attachment_name=None):
     if not to_email :
          print("Warning : No email found")
          return False
     
     params = {
          "from": "E-Visual Gallery <onboarding@resend.dev>",
          "to" :[to_email],
          "subject" : subject,
          "html" : html_content
     }

     if attachment_path and attachment_name and os.path.exists(attachment_path):
          try:
               with open(attachment_path, 'rb') as f :
                    data = f.read()
               encoded = base64.b64encode(data).decode("utf-8")
               params["attachments"] = [{
                    "filename":attachment_name,
                    "content":encoded,
                    "type": "image/jpeg"
               }]
               print(f"attachment added {attachment_name}")
          except Exception as error:
               print(f"Error : image not attached as : {error}")
     try :
          response = resend.Emails.send(params)
          print(f"Email done to {to_email} ID {response.get('id','unknown')}")
          return True
     except Exception as send_err :
          print(f"Error : {send_err}")



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

          success = send_gallery_email(
               to_email= admin_email,
               subject=f"Delete Request: {image_name}",
               html_content= html_content,
               attachment_path= filepath if os.path.exists(filepath) else None,
               attachment_name= image_name if os.path.exists(filepath) else None
          )

          if success :
               return jsonify({"message" : "Request sent successfully, it will take at most two working days to approve your reqest :)"}) , 200
          else :
               return jsonify({"message": "Failed to send email. Please try again later."}), 500
          
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
              send_gallery_email(
                    to_email= email,
                    subject= "Your photo from E-Visual Gallery",
                    html_content= html_content,
                    attachment_path= filepath,
                    attachment_name= filename
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



