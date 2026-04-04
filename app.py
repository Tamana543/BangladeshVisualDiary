#draft_codes.txt
from pymongo import MongoClient
import os
import threading
from flask import Flask,render_template, request, jsonify
from flask_mail import Mail,Message 
import traceback
from smtplib import SMTPException

import requests






# MongoDb setup 
MONGO_URI = os.environ.get("MONGO_URI", "mongodb://localhost:27017/my_database")
client = MongoClient(MONGO_URI)
db = client['e_gallery_database']
photos_collection = db['photos']

# Flask Hundler 

app = Flask(__name__) 

# ImgFolder config
UPLOAD_FOLDER = "static/default_images"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER 

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
    print(f"Created folder: {UPLOAD_FOLDER}")



# Email handler (brevo)
app.config['MAIL_SERVER'] = os.environ.get('BREVO_SMTP_HOST', 'smtp-relay.brevo.com')
app.config['MAIL_PORT'] = int(os.environ.get('BREVO_SMTP_PORT', 587))
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = os.environ.get('BREVO_SMTP_USER')
app.config['MAIL_PASSWORD'] = os.environ.get('BREVO_SMTP_PASS')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('BREVO_SMTP_USER')
app.config['MAIL_TIMEOUT'] = 10

mail = Mail(app)

# Email Function 
# def send_gallery_email(to_email, subject, html_content, attachment_path=None, attachment_name=None) :
#      if not to_email :
#           print("Warning: No email provided")
#           return False
#      try :
#           with mail.connect() as conn:
#                msg = Message(
#                     subject=subject,
#                     recipients=[to_email],
#                     html=html_content,
#                     sender=("E-Visual Gallery", os.environ.get('BREVO_SMTP_USER'))
#                )
#                if attachment_path and os.path.exists(attachment_path):
#                          with open(attachment_path, "rb") as f:
#                               msg.attach(attachment_name, "image/jpeg", f.read())
#                conn.send(msg)         
          
#           print(f"👩 Success: email send to : {to_email}")
               

#      except Exception as error :
#                print(f"Failed: Email Error {error}")
#                traceback.print_exc()
               
     
#      # thread = threading.Thread(target=send_email_thread)
#      # thread.daemon = True
#      # thread.start()
    
#      return True 



def send_gallery_email(to_email, subject, html_content, attachment_path=None, attachment_name=None):
    api_key = os.environ.get("BREVO_API_KEY")

    if not api_key:
        print("No API key found")
        return False

    url = "https://api.brevo.com/v3/smtp/email"

    headers = {
        "accept": "application/json",
        "api-key": api_key,
        "content-type": "application/json"
    }

    data = {
        "sender": {
            "name": "E-Visual Gallery",
            "email": os.environ.get("BREVO_SMTP_USER")
        },
        "to": [{"email": to_email}],
        "subject": subject,
        "htmlContent": html_content
    }

    response = requests.post(url, json=data, headers=headers)

    print("Status:", response.status_code)
    print("Response:", response.text)

    return True

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
          admin_email = os.environ.get('BREVO_SMTP_USER')

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

          thread = threading.Thread(
               target=send_gallery_email,
               args=(
                    admin_email,
                    f"Delete request for : {image_name}",
                    html_content,
                    # filepath if os.path.exists(filepath) else None,
                    # image_name if os.path.exists(filepath) else None
               )
               )
          thread.daemon = True
          thread.start()

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
     valid_photos = [
          photo for photo in photos 
          if os.path.exists(os.path.join(app.config["UPLOAD_FOLDER"],photo.get('filename', '')))
          ]
     
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
              thread = threading.Thread(
                    target=send_gallery_email,
                    args=(email,
                              "Your photo from E-visual Gallery",
                              html_content,
                              # filepath,
                              # filename
                              )
                    )
              thread.daemon = True
              thread.start()
            
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



