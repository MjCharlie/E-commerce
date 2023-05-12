from flask import Flask, config, render_template, request, redirect
from flask_mail import Mail
# from flask.wrappers import Request
import os
from flask_sqlalchemy import SQLAlchemy
import json
from werkzeug.utils import secure_filename
with open("config.json", "r") as c:
    params = json.load(c)["params"]
app = Flask(__name__)
loged = False
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
app.config['SQLALCHEMY_DATABASE_URI'] = params["local_uri"]
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['UPLOAD_FOLDER'] = params["UPLOAD_LOCATION"]
db = SQLAlchemy(app)
app.config.update(
    MAIL_SERVER = 'smtp.google.com',
    MAIL_PORT = '465',
    MAIL_USE_SSL = True,
    MAIL_USERNAME = params["gmail_user"],
    MAIL_PASSWORD = params["gmail_password"]
)
mail =Mail(app)
class U_id(db.Model):
    # sno name password descr
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(50), nullable=False)
    passw = db.Column(db.String(25), nullable=False)
    descr = db.Column(db.String(500), nullable=False)
    file_img = db.Column(db.String(500), nullable=True)

    # def __repr__(self):
    #     return '<User %r>' % self.

@app.route('/mail', methods=['GET', 'POST'])
def mailer():
    mail.send_message("no-reply", 
    sender=params["gmail_user"] , 
    recipients= "kartavyamaheshwariapsf21@gmail.com",
    body="hello just checking wether it works or not"
    )
    return "sended"
@app.route('/uploader', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        f = request.files['file1']
        f.save(os.path.join(
            app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))
        # print(f.filename)
    return render_template('upload.html')


@app.route('/qry', methods=['GET', 'POST'])
def qry():
    t = U_id.query.all()
    for i in t:
        print(i.name)
    return redirect('/')


@app.route('/watch', methods=['GET', 'POST'])
def watch():
    if request.method == 'POST':
        k = request.form['ur']
        rt = U_id.query.filter_by(user_name=k).first()
        return render_template("watch.html", rt=rt)
    return "<form action='/watch' method='post'> <input name='ur' type='text' > <input  type='submit'> </form>"


@app.route('/light', methods=['GET', 'POST'])
def light():
    return render_template('ot2.html')


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        name = request.form.get('user')
        passw = request.form.get('passw')
        desc = request.form.get('desc')
        f = request.files['file1']
        f.save(os.path.join(
            app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))
        entry = U_id(user_name=name, passw=passw,
                     descr=desc, file_img=f.filename)
        db.session.add(entry)
        db.session.commit()
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True,port=5000)
