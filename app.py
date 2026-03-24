#any confussion check draft_codes.txt
from flask_mail import Mail, Message
#DataBase Hundler
import sqlite3 # main sql :)
def init_db():
     with sqlite3.connect("database.db") as data_table :
          data_table.execute("""
               CREATE TABLE IF NOT EXISTS photos(
                             id INTEGER PRIMARY KEY AUTOINCREMENT, 
                             filename TEXT NOT NULL, 
                             description TEXT NOT NULL, 
                             sender TEXT NOT NULL
               )
          """)



# Flask Hundler 
import os
from flask import Flask, render_template,request,jsonify

app = Flask(__name__) 

# Email handler 

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587 
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'auw242106@auw.edu.bd'
app.config['MAIL_PASSWORD'] = 'okkn jnwz iyie xpkz'
app.config['MAIL_DEFAULT_SENDER'] = 'auw242106@auw.edu.bd'

mail = Mail(app)


@app.route("/") 
def main():
     # return "Hello" 
     return render_template("index.html")

@app.route("/edit_req")
def edit_req():
     return render_template("edit_req.html")


@app.route("/api/delete_request", methods=['POST'])
def delete_request():
     data = request.get_json()

     sender_name = data.get('sender')
     image_name = data.get('imageName')
     reason = data.get('reason')

     
     

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
     


UPLOAD_FOLDER = "static/default_images"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER 
@app.route("/api/photos") 
def photo_render():
     data = sqlite3.connect("database.db")
     data.row_factory = sqlite3.Row
     photos = data.execute('SELECT * FROM photos').fetchall()
     data.close()
     return jsonify([dict(photo) for photo in photos]) 


@app.route("/api/photos", methods=['POST'])
def photo_upload():
     file= request.files["file"]
     description = request.form["description"]
     sender = request.form["sender"]
     email = request.form.get("email")

     filename = file.filename
     filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
     file.save(filepath)

     
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
     #SQL hundler
     connection = sqlite3.connect("database.db")
     conn_cursor = connection.cursor()

     conn_cursor.execute("""
          INSERT INTO photos (filename,description,sender) VALUES (?,?,?)

     """,(filename,description,sender))
     connection.commit()
     connection.close()

     return { "message": "Done uploadeing "}, 201
    

@app.errorhandler(404)
def error_page(error):
     return render_template("404.html"), 404


init_db()
if __name__ == "__main__":
    app.run(debug=True) 


# http://127.0.0.1:5000
