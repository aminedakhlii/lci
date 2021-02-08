from globals import db


class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course = db.Column(db.String(20), nullable=False)
    type = db.Column(db.String(20), nullable=False)
    company = db.Column(db.String(30), nullable=False)
    hours = db.Column(db.Integer,  nullable=False)
    professor = db.Column(db.Integer, db.ForeignKey('professor.id'), nullable=False)
    book = db.Column(db.String(30),  nullable=False)
    place = db.Column(db.String(30),  nullable=False)
    price = db.Column(db.String(10),  nullable=False)
    start = db.Column(db.DateTime, nullable=False)
    end = db.Column(db.DateTime, nullable=False)
    weekly = db.Column(db.Integer,  nullable=True)
    days = db.Column(db.String(10),  nullable=True)
    checked = db.Column(db.Boolean, default=True)
    hoursPerSession = db.Column(db.Float , default=2)
    comment = db.Column(db.String(100),  nullable=True)

class Professor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30),  nullable=False)
    email = db.Column(db.String(50) )
    phone = db.Column(db.String(15) )
    recapHours = db.Column(db.Integer , nullable=True)
    courses = db.relationship('Course', backref='teacher', lazy=True)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fullName = db.Column(db.String(50) , nullable=False)
    email = db.Column(db.String(50) , nullable=False)
    phone = db.Column(db.String(15) , nullable=False)

class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    studentId = db.Column(db.Integer , nullable=False)
    courseId = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Boolean)
