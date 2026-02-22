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

def test_data():
     with sqlite3.connect("database.db") as test_data:
          test_data.execute("""
            INSERT INTO photos (filename, description, sender)
            VALUES ('test.jpg', 'Test Description', 'Tamana')
        """)

# Flask Hundler 
import os
from flask import Flask, render_template,request,jsonify

app = Flask(__name__) # import flask 


@app.route("/") # to create the web application and if someone visited  the homepage /, run the function below
def main():
     # return "Hello" # if you see this in http://127.0.0.1:5000 url, means everything is okay in backend 
     return render_template("index.html")

#defines the directory on the server where all uploaded files will be stored
Upload_folder = "static/default_images"
app.config["Upload_folder"] = Upload_folder #make the specified upload path accessible throughout your Flask application's views and logic. (by storing it in app.config)
@app.route("/api/photos") # in this route it connect to database and get photos 
def photo_upload():
     

     # with no file follow this 
     '''
     data = sqlite3.connect("database.db")
     # to make rows to be like dictionaries so that it can be used as a json 
     data.row_factory = sqlite3.Row
     photos = data.execute('SELECT * FROM photos').fetchall()
     data.close()
     return jsonify([dict(photo) for photo in photos]) # to check if everything is good visite http://127.0.0.1:5000/api/photos
     '''


@app.route("/api/photos", methods=['POST'])
def photo_upload():
     #fetching data 
     data = request.json
     filename = data['filename']
     description =data['description']
     sender = data['sender']

     #call database
     databse_connector = sqlite3.connect('database.db')
     database = databse_connector.cursor()
     database.execute("""
          INSERT INTO photos(filename,description,sender) VALUES (?,?,?)

     """,(filename,description,sender))

     databse_connector.commit()
     databse_connector.close()

     return { "message": "Done uploadeing "}, 201



init_db()
# test_data()
if __name__ == "__main__":# function as both a reusable module
    app.run(debug=True) # executed only when the script is run directly

