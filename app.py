import os

from flask import Flask, render_template, request, flash, redirect
from werkzeug.utils import secure_filename

from image_handler import encode, decode

app = Flask(__name__)

# setting up session key
app.secret_key = 'secret key'
print(os.getcwd())

UPLOAD_FOLDER = './static/images/'
DECODE_FOLDER = './static/decoded/'
ENCODED_OUTPUT = './static/encoded/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DECODE_FOLDER'] = DECODE_FOLDER
app.config['ENCODED_OUTPUT'] = ENCODED_OUTPUT


@app.route("/")
def home():
    return render_template("index.html")


@app.route('/encode', methods=['GET', 'POST'])
def encode_handler():
    if request.method == 'GET':
        return render_template('encode.html')
    elif request.method == 'POST':
        if 'file' not in request.files or request.form.get('message') == '':

            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':

            return redirect(request.url)
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            # encoding part
            message = request.form.get("message")
            m = encode(filename, message, filename)

            return download_file(filename)

    return render_template('encode.html')


# We want to be able to serve the uploaded files so they can
# be downloaded by users. We’ll define a download_file view to
# serve files in the upload folder by name. url_for("download_file", name=name)
# generates download URLs.

@app.route('/encoded')
def download_file(name):
    return render_template('download.html', filename=app.config['ENCODED_OUTPUT'] + name)


# Decoding part
@app.route('/decode', methods=['GET', 'POST'])
def decode_handler():
    if request.method == 'GET':
        return render_template('decode_form.html')

    elif request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['DECODE_FOLDER'], filename))

            # do decode
            message = decode(filename)

            return render_template('decode_message.html', message=message, image='static/decoded/' + filename)
    return render_template('decode_form.html')


@app.errorhandler(404)
def handle_page_not_found(e):
    return render_template("error_404.html",
                           error_message='404 Not Found: The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.')


@app.errorhandler(Exception)
def handleTypeError(e):
    return render_template("error.html", message=str(e))


app.run(port=8081, debug=True)
