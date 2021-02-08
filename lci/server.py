from flask import Flask , request , render_template , redirect, flash , url_for , redirect
from forms import addCourseForm , addProfForm , addStudentForm, ModifyProfForm
from models import Course , Room , Student , Professor
import difflib, datetime
from globals import app, db
from certifs import Doc


@app.route('/')
def overview():
    coursesDemo = Course.query.order_by(Course.start.desc()).limit(5).all()

    profsDemo = Professor.query.order_by(Professor.name).limit(3).all()

    studentsDemo = Student.query.order_by(Student.fullName).limit(3).all()

    profs = Professor.query.order_by(Professor.id).all()

    db.session.commit()

    profs = []

    for course in coursesDemo:
        profs.append(Professor.query.filter_by(id=course.professor).first())

    db.session.commit()
    profsDemo = [p.name for p in profsDemo]
    studentsDemo = [s.fullName for s in studentsDemo]

    return render_template('index.html' , courses=coursesDemo, teachers=profs , profs = profsDemo , students=studentsDemo)



def checkExistingRoom(sid,cid):
    room = Room.query.filter_by(courseId=cid , studentId = sid).first()
    db.session.commit()
    if room:
        return True
    return False

@app.route('/addStudent/<course_id>/<fromOld>/<int:id>' , methods=['GET' , 'POST'])
def addStudent(course_id, fromOld, id):


    form = addStudentForm()

    if form.validate_on_submit():
        exist = Student.query.filter_by(fullName=form.name.data).first()
        db.session.commit()

        if exist:
            if checkExistingRoom(exist.id , course_id):
                print('existant')
                pass
            else:
                room = Room(courseId=course_id , studentId = exist.id , status=False)
                db.session.add(room)
                db.session.commit()
        else:
            s = Student(fullName=form.name.data , email=form.email.data,phone=form.phone.data)
            nbr = Student.query.count()
            room = Room(courseId=course_id , studentId = nbr+1, status=False)
            db.session.add(s)
            db.session.add(room)
            db.session.commit()
        return redirect(url_for('courseDetails' , course_id=course_id))
    elif fromOld and id != 0:
        print(id)
        s = Student.query.filter_by(id=id).first()
        if checkExistingRoom(s.id , course_id):
            print('here')
            pass
        else:
            room = Room(courseId=course_id , studentId = s.id)
            db.session.add(room)
            db.session.commit()
        return redirect(url_for('addStudent' , course_id=course_id , fromOld=False , id=0))

    return render_template('modifyStudent.html' , form=form , id=course_id)



@app.route('/prof/<int:prof_id>' , methods=['GET' , 'POST'])
def profModify(prof_id):
    currentProf = Professor.query.filter_by(id=prof_id).first()
    form = ModifyProfForm()
    if form.validate_on_submit():
        currentProf.name = form.name.data
        currentProf.phone = form.phone.data
        currentProf.email = form.email.data
        currentProf.recapHours = form.recapHours.data
        db.session.commit()
        return redirect(url_for('profs'))
    return render_template('modifyProf.html' , form = form , prof= currentProf)


@app.route('/profs')
def profs():
    profs = Professor.query.order_by(Professor.name).all()
    for prof in profs:
        courses = Course.query.filter_by(professor=prof.id).all()
        recap = 0
        if courses:
            for course in courses:
                tmp = howManyCourseDays(course)
                if tmp > 0:
                    recap += tmp
        prof.recapHours = recap
    db.session.commit()
    return render_template('teachers.html' , profs=profs)

def howManyCourseDays(course):
    if str(course.days) == 'None':
        return -1
    days = str(course.days)[:-1]
    days = days.split(',')
    days = [int(i) for i in days]
    days = [i-1 for i in days]
    begin = course.start
    end = datetime.datetime.today() # + datetime.timedelta(days=1
    diff = (end-begin).days #doesn't consider today !
    if diff < 0:
        return  -1
    day_of_week = begin.weekday()
    numSessions= len(days)*(diff//7)
    for i in range(diff%7):
        if day_of_week in days:
            numSessions += 1
        day_of_week = (day_of_week +1) %7
    if course.hoursPerSession:
        print(days)
        print(numSessions  )
        return numSessions * course.hoursPerSession
    return numSessions * 2


@app.route("/search")
def search():
    username = request.args.get('search' , '' )
    student = Student.query.filter_by(fullName=username).first()
    if student:
        suggestions = student
    else:
        students = Student.query.all()
        suggestions = []
        for s in students:
            if username.lower() in s.fullName.lower():
                suggestions.append(s)
    db.session.commit()
    return render_template('search.html' , user=suggestions)


@app.route('/students/<int:existing>')
def students(existing):
    students = Student.query.order_by(Student.fullName).all()
    db.session.commit()

    if existing == 0:
        return render_template('students.html' , students=students , existing=False )
    else:
        return render_template('students.html' , students=students , existing=existing )


@app.route('/studentCourses/<int:sid>')
def studentCourses(sid):
    coursesIds = Room.query.filter_by(studentId=sid).all()
    student = Student.query.filter_by(id=sid).first()

    status = []

    for course in coursesIds:
        status.append(course.status)


    coursesIds = [c.courseId for c in coursesIds]
    name = student.fullName

    db.session.commit()

    courses = []
    for id in coursesIds:
        potential = Course.query.filter_by(id=id).first()
        db.session.commit()
        courses.append(potential)

    profs = []

    for course in courses:
        profs.append(Professor.query.filter_by(id=course.professor).first())

    db.session.commit()

    return render_template('studentCourses.html' , name=name , courses=courses , profs=profs ,  stats = status)


@app.route('/addProf' , methods=['GET','POST'])
def addProf():
    form = addProfForm()
    if form.validate_on_submit():
        prof = Professor(name= form.name.data , email=form.email.data , phone=form.phone.data , recapHours = 0)
        db.session.add(prof)
        db.session.commit()
        flash('Professor added successfully' , 'success')
        return redirect(url_for('profs'))
    return render_template('addTeacher.html' , form=form)

import courseRoutes
