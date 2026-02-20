#DataBase Hundler
import sqlite3 # main sql :)
def init_db():
     with sqlite3.connect("database.db") as data_table :
          data_table.execute("""
               CREATE TABLE IF NOT EXISTS photos(
                             id INTEGER PRIMARY KEY AUTO_INCREMENT, 
                             filename TEXT NOT NULL, 
                             description TEXT NOT NULL, 
                             sender TEXT NOT NULL
                             )
                         """)

# Flask Hundler 
from flask import Flask, render_template

app = Flask(__name__) # import flask 

@app.route("/") # to create the web application and if someone visited  the homepage /, run the function below
def main():
     # return "Hello" # if you see this in http://127.0.0.1:5000 url, means everything is okay in backend 
     return render_template("index.html")

init_db()

if __name__ == "__main__":# function as both a reusable module
    app.run(debug=True) # executed only when the script is run directly

