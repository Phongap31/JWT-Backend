from flask import Flask, request, jsonify, session
from flask_jwt_extended import create_access_token, create_refresh_token, JWTManager
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
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

class StudentSchema(Schema):
    id = fields.Int()
    fullname = fields.Str()
    birthday = fields.Date()
    email = fields.Str()
    level = fields.Str()

@app.route('/register', methods = ['POST'])
def register():
    params = json.loads(request.data)
    username = params['username']
    password = bcrypt.generate_password_hash(params['password']).decode('utf-8')
    email = params['email']

    found_user = User.query.filter_by(username=username).first()
    if found_user:
        return 'username exists!'

    userab = User(username = username, password = password, email = email)
    db.session.add(userab)
    db.session.commit()

    return 'Register Successful!!'

@app.route('/login', methods = ['POST'])
def login():
    params = json.loads(request.data)
    found_user = User.query.filter_by(username = params['username']).first()
    result = ''

    if found_user:
        if bcrypt.check_password_hash(found_user.password, params['password']):
            access_token = create_access_token(identity = {
                'username': found_user.username,
                'email': found_user.email
            })
            result = jsonify({'token': access_token})
        else:
            result = jsonify({'error': 'Email or password incorrect!'})
    else:
        result = jsonify({'error': 'User not found!!'})

    return result

@app.route('/api/change_pass', methods = ['POST'])
def change_password():
    params = json.loads(request.data)
    print(params)
    found_user = User.query.filter_by(username = params['username']).first()

    if found_user:
        if bcrypt.check_password_hash(found_user.password, params['currentP']):
            found_user.password = bcrypt.generate_password_hash(params['newP']).decode('utf-8')
            db.session.commit()
            return jsonify({'result': 'Change Password Success!'})
        else:
            return 'Password incorrect!'
    else:
        return 'User Not Found!'

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
    params = json.loads(request.data)
    fullname = params['fullname']
    birthday = params['birthday']
    email = params['email']
    level = params['level']

    found_student = Student.query.filter_by(email=email).first()

    if found_student:
        return jsonify({'result':'Student exist!'})
    
    student = Student(fullname = fullname, birthday = birthday, email = email, level = level)
    db.session.add(student)
    db.session.commit()
    return jsonify({'result': 'Addition Successful!'})

@app.route('/api/update/<id>', methods = ['POST'])
def update(id):
    params = json.loads(request.data)
    found_stu = Student.query.filter_by(id=id).first()

    found_stu_by_email = Student.query.filter_by(email = params['email']).first()

    if found_stu_by_email:
        return jsonify({'result': 'Email exist!'})
    else:
        found_stu.fullname = params['fullname']
        found_stu.birthday = params['birthday']
        found_stu.email = params['email']
        found_stu.level = params['level']

        db.session.commit()
        return jsonify({'result': 'Update Success!'})


@app.route('/api/get_current/<id>', methods = ['GET'])
def get_current(id):
    found_stu = Student.query.filter_by(id=id).first()
    studentSchema = StudentSchema()
    stu = studentSchema.dump(found_stu)
    
    return jsonify(json.dumps(stu))

@app.route('/api/delete_stu/<id>', methods = ['DELETE'])
def delete_stu(id):
    found_del = Student.query.filter_by(id = id).first()
    if found_del:
        db.session.delete(found_del)
        db.session.commit()
        return jsonify({'result': 'Delete Successful!'})
    else:
        return jsonify({'result':'Student Not Found!'})

if __name__ == "__main__":
    db.__init__(app)
    app.run(debug=True)