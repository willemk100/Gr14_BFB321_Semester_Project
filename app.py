from flask import Flask, render_template

import sqlite3

app = Flask(__name__)

@app.route("/")
def login():
    return render_template("login.html")

if __name__ == '__name__':
    app.run()