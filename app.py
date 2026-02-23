#any confussion check draft_codes.txt
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


@app.route("/") 
def main():
     # return "Hello" 
     return render_template("index.html")

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

     filename = file.filename

     file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

     #SQL hundler
     connection = sqlite3.connect("database.db")
     conn_cursor = connection.cursor()

     conn_cursor.execute("""
          INSERT INTO photos (filename,description,sender) VALUES (?,?,?)

     """,(filename,description,sender))
     connection.commit()
     connection.close()

     return { "message": "Done uploadeing "}, 201
    



init_db()
if __name__ == "__main__":
    app.run(debug=True) 

