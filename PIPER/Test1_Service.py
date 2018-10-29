import os
from flask import Flask, request, jsonify, render_template, redirect, url_for, Markup, flash
from werkzeug.utils import secure_filename
import subprocess

UPLOAD_FOLDER = 'uploads\\DAT_IN'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'dat'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'super secret key'

# @app.route('/', methods=['GET', 'POST'])
# def home():
#     if request.method == 'POST':
#         try:
#             data = request.get_json()
#
#         except ValueError:
#             return jsonify("Please enter a number.")
#
#         return jsonify([x * 2 for x in data])
#     elif request.method == 'GET':
#         return render_template("home.html")

@app.route('/about', methods=['GET', 'POST'])
def about():
    return render_template("home.html")

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_files():
    if request.method == 'POST':
        uploaded_files = request.files.getlist("file[]")
        for file in uploaded_files:
            filename = (file.filename)
            print(os.path)
            print(app.config['UPLOAD_FOLDER'])
            print(filename)
            newName = app.config['UPLOAD_FOLDER'] + '\\' + filename
            file.save(newName)
            # file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # return render_template("upload.html")
        #return redirect(url_for('upload_files', filename=filename))

    return render_template("home.html")

@app.route('/runpiper',  methods=['GET', 'POST'])
def runpiper():
    print("PIPER starts:")
    message = "PIPER starts:" + "<br />\n"
    flash(Markup(message))

    process = subprocess.Popen("TestDriverC.exe", stdout=subprocess.PIPE)
    while True:
        output = process.stdout.readline()
        if process.poll() is not None:
            break
        if output:
            message = Markup(output.strip().decode("utf-8")+ "<br />\n")
            flash(message)

    rc = process.poll()

    print("PIPER completes!")
    message = Markup("PIPER completes!" + "<br />\n")
    flash(message)
    return render_template('home.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0')