from flask import Flask, request, jsonify, session
from flask_jwt_extended import create_access_token, create_refresh_token
from flask_bcrypt import Bcrypt
from werkzeug.security import check_password_hash, generate_password_hash
from models import *
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields
from datetime import date
import json
from flask_cors import CORS

app = Flask(__name__)
app.secret_key = "okbro"
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://zvblamkcuzqqar:fe41bf1d9ef070c35ba1670bf172a6a3ca3b3af568eef0cd1548141259c6a804@ec2-54-158-222-248.compute-1.amazonaws.com:5432/detgrr1hkbgiv9'
CORS(app)

class StudentSchema(Schema):
    id = fields.Int()
    fullname = fields.Str()
    birthday = fields.Date()
    email = fields.Str()
    level = fields.Str()

@app.route('/register')
def register():
    username = request.get_json()['username']
    email = request.get_json()['email']
    password = Bcrypt.generate_password_hash(request.get_json()['password']).decode('utf-8')

    found_user = User.query.filter_by(username=username).first()
    if found_user:
        return 'username exists!'

    user = User(username = username, email = email, password = password)
    # all_user = User.query.order_by(User.username).all()
    # print(all_user)
    # user_limit = User.query.limit(1).all()
    # print('user: ', user_limit)
    db.session.add(user)
    db.session.commit()

    return 'Register Successful!!'

@app.route('/api/get_all', methods = ["GET"])
def get_all():
    listStudent = []
    all_student = Student.query.all()
    studentSchema = StudentSchema()
    for x in range(len(all_student)):
        stu = studentSchema.dump(all_student[x])
        listStudent.append(stu)

    return jsonify(json.dumps(listStudent))

@app.route('/api/add_stu', methods = ['POST'])
def add_stu():
    fullname = request.get_json()['fullname']
    birthday = request.get_json()['birthday']
    email = request.get_json()['email']
    level = request.get_json()['level']

    found_student = Student.query.filter_by(email=email).first()

    if found_student:
        return 'Student exist!'
    
    student = Student(fullname, birthday, email, level)
    db.session.add(student)
    db.session.commit()
    return 'Addition Successful!'


@app.route('/api/delete_stu/<id>', methods = ['POST'])
def delete_stu(id):
    found_del = Student.query.filter_by(id = id).first()
    if found_del:
        db.session.delete(found_del)
        db.session.commit()
        return 'Delete Successful!'
    else:
        return 'Student Not Found!'

if __name__ == "__main__":
    db.__init__(app)
    app.run(debug=True)