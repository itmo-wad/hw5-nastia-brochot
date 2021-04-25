from flask import Flask, render_template, redirect, url_for, request, flash, send_from_directory, send_file
from pymongo import MongoClient
from flask_bootstrap import Bootstrap
import os
from werkzeug.utils import secure_filename

client = MongoClient('localhost', 27017)
db = client.hw4
import json

app = Flask(__name__)

UPLOAD_FOLDER = 'upload'

app.secret_key = "this is the secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/static/<path:path>')
def image(path):
    return app.send_static_file(path)

@app.route('/', methods=['GET', 'POST'])
def login():
    user = db.user.find_one({})
    error = None
    username = user['username']
    password = user['password']
    if request.method == 'POST':
        if request.form['username'] != username or request.form['password'] != password:
            error = 'Invalid Credentials. Please try again.'
        else:
            return "You are connected"
    return render_template('login.html', error=error)


@app.route('/cabinet', methods=["GET", "POST"])
def cabinet():
    password = db.user.find({})
    if request.method == "POST":
        if 'file' not in request.files:
            flash('No file part', 'danger')
            return redirect(request.url)
            
        file = request.files['file']
        if file.filename == '':
            flash('No selected file', 'danger')
            return redirect(request.url)
            
        if not allowed_file(file.filename):
            flash('Invalid file extension', 'danger')
            return redirect(request.url)
            
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
            flash('Successfully saved', 'success')
            return 'File uploaded'
        else:
            flash("Alliwed image types are : txt, pdf, png, jpg, jpeg, gif")
            return render_template("cabinet.html")

    if request.method == "GET":
        return render_template("cabinet.html", password=password)

@app.route('/upload/<path:filename>')
def uploaded_file(filename):
    print("ok")
    print(app.config['UPLOAD_FOLDER'])
    return send_file(os.path.join(app.config['UPLOAD_FOLDER'], filename))


if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)