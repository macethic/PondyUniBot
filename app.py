import os, threading
from university_final_copy import *
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug import secure_filename


app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['RESULT_FOLDER'] = 'result/'
app.config['ALLOWED_EXTENSIONS'] = set(['txt'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

def process_data(filename, text):
	print "entering data processing..."
	PondyUniBot('uploads/' + filename, text)
@app.route('/')
def index():
    return render_template('index.html')

@app.route
@app.route('/upload', methods=['POST'])
def upload():
	
	file = request.files['file']
	if file and allowed_file(file.filename):
        	
		text = request.form['text']
		filename = secure_filename(file.filename)
        	
		file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
		t = threading.Thread(target=process_data, args=(filename, text))
		t.start()
		return render_template('progress.html',useremail = text)

if __name__ == '__main__':
	app.run(
        host="0.0.0.0",
        port=int("80"),
        debug=True
    )
