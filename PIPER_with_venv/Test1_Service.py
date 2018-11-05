from flask import Flask, request, render_template, Markup, flash
import subprocess

UPLOAD_FOLDER = 'uploads\\DAT_IN'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'super secret key'

@app.route('/', methods=['GET', 'POST'])
def upload_files():
    if request.method == 'POST':
        uploaded_files = request.files.getlist("file[]")
        for file in uploaded_files:
            filename = (file.filename)
            file.save(app.config['UPLOAD_FOLDER'] +'//'+ filename)

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