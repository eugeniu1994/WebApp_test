from flask import Flask, render_template, \
    request, jsonify, send_file, session
from db.dataBase import checkUser, execute_once
import os
import base64
import pandas as pd
#from werkzeug import secure_filename
from werkzeug.utils import secure_filename
from main import main

app = Flask(__name__)
app.secret_key = "my super secret key"

@app.route("/")
def logIn():
    if 'user' in session:
        user = session['user']
        return render_template('home.html', user=user)

    return render_template('LogIn.html')

@app.route('/checkUserLogIn', methods=['GET', 'POST'])
def checkUserLogIn():
    msg, status = '', False
    try:
        user = request.form['txtUsername']
        password = request.form['txtPass']
        status = checkUser(username=user, password=password)
        if status:
            session['user'] = user
            msg = 'successfully logged in'
        else:
            session.pop('user', None)
            msg = 'wrong username or password'
    except:
        session.pop('user', None)
        msg, status = 'Internal server error', False

    if status:
        return render_template('home.html', user=user)

    return jsonify({'status': status, 'msg': msg})

def remove_old_files(file=None):
    try:
        if file is not None:
            if os.path.exists(file):
                os.remove(file)
                print(file + ' removed')
            else:
                print(file + " does not exist")
    except:
        print('treat the error here')

@app.route('/upload_document', methods=['POST', 'GET'])
def upload_document():
    if 'user' not in session:
        return
    status, msg, encoded_img, csv_table = False, "", "", ""
    if 'files' not in request.files:
        msg, status = 'No files', False
        return jsonify({'msg': msg, 'status': status})

    files = request.files.getlist('files')
    csv = files[0]

    filename = secure_filename(csv.filename)  # make it safe
    if '.' not in filename or filename.rsplit('.', 1)[1].lower() != 'csv':
        msg, status = 'Not a csv file', False
        return jsonify({'msg': msg, 'status': status})

    save_folder = './save_folder'
    try:
        csv.save(os.path.join(save_folder, filename))

        main(os.path.join(save_folder, filename))

        img_name = './output.png'
        with open(img_name, "rb") as image_file:
            encoded_img = base64.b64encode(image_file.read())

        table = pd.read_csv("./output.csv")
        csv_table = table.to_html()

        msg, status = 'ok', True
    except:
        msg, status = 'Server error -> main', False

    remove_old_files(file=os.path.join(save_folder, filename))
    remove_old_files(file='./output.png')

    result = {"csv_table": csv_table, "encoded_img": encoded_img, "msg": msg, "status": status}
    return jsonify(result)

@app.route("/getCsv")
def getCsv():
    if 'user' not in session:
        return
    try:
        csv = send_file('./output.csv',
                        mimetype='text/csv',
                        attachment_filename='output.csv',
                        as_attachment=True)
        remove_old_files(file='./output.csv')
        return csv
    except:
        print('treat the error here')

@app.route("/logOff")
def logOff():
    session.pop('user', None)
    return render_template('LogIn.html')


if __name__ == "__main__":
    app.run(debug=True)
