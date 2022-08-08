from copy import error
from wsgiref.util import request_uri
from flask import Flask, render_template, request
import numpy as np
import pickle
import os
import requests
from werkzeug.utils import secure_filename
import json
from matplotlib.font_manager import json_load

d=json_load("login.json")




#app.config.from_pyfile('./static/schema.ini', silent=True)




app = Flask(__name__)


SYS=d[0]['name']
ADMIN=d[1]['name']
SYS_PS=d[0]['word']
ADMIN_PS=d[1]['word']


app.config["UPLOAD_FOLDER"] = "dataset/"

model = pickle.load(open('model.pkl', 'rb'))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    val1 = request.form['LotArea']
    val2 = request.form['OverallQual']
    val3 = request.form['OverallCond']
    val4 = request.form['YearBuilt']
    
    try:
        
        arr = np.array([val1, val2, val3, val4])
        arr = arr.astype(np.float64)
        pred = model.predict([arr])
        
    except:
            pred=0
    return render_template('index.html', data=int(pred))


@app.route('/upload', methods=['POST'])
def load_file():
    if request.method == 'POST':
        f = request.files['file']
        filename = secure_filename(f.filename)
        if os.path.exists(filename):
            os.remove(app.config["UPLOAD_FOLDER"] + filename)
        else:
            f.save(app.config["UPLOAD_FOLDER"] + filename)
        return render_template("admin.html")    
@app.route('/read', methods=['GET'])
def process_read():
    return render_template("user.html")
@app.route('/read', methods=['POST'])
def process():
    _username = request.form.get('_username')
    _filename = request.form.get('_filename')
    if _username == SYS:
        file = open(app.config["UPLOAD_FOLDER"] + _filename, "r")
        content = file.read()
        return render_template('content.html', content=content)
    else:
        return 'Please go back and enter your name...', 400 

@app.route('/admin', methods=['GET'])
def process_train():
    return render_template("admin.html")
@app.route('/admin', methods=['POST'])
def process_train_post():
    _username = request.form.get('_username')
    _password = request.form.get('_password')
    
    #filename = os.path.join(app.instance_path, 'schema.ini')
    if _username == SYS and _password==SYS_PS:
            return render_template('upload.html')
    elif _username == ADMIN and _password==ADMIN_PS:
            os.system("python price_predict.py")
            return render_template("index.html")
    else:
            return 'Please go back and enter your name...', 400 
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'),404
@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'),500

if __name__ == '__main__':
    
    app.run()
