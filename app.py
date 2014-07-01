import os, threading
from university_final_copy import *
from sendmail import *
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug import secure_filename


app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['RESULT_FOLDER'] = 'result/'
app.config['ALLOWED_EXTENSIONS'] = set(['txt'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']


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
		return render_template('progress.html')
		
PondyUniBot('uploads/' + 'reg2.txt')
mail("vikneshwaren.u@gmail.com",
   "Pondicherry University marks",
   "Please check out the attachment!, Thanks for using my service!",
   "result/output.csv")

if __name__ == '__main__':
    app.run(
        host="0.0.0.0",
        port=int("80"),
        debug=True
    )

