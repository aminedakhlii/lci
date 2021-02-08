from imports import *
from certifs import Doc
import datetime , os

@app.route('/courses')
def courses():
    courses = Course.query.order_by(Course.id.desc()).all()
    pids = [p.professor for p in courses]
    names = []
    for p in pids:
        names.append(Professor.query.filter_by(id = p).first())
    db.session.commit()
    return render_template('courses.html' , courses=courses , names=names)

@app.route('/addCourse' , methods=['POST' , 'GET'])
def addCourse():
    form = addCourseForm()
    if form.validate_on_submit():
        daysStr = ''
        for day in form.days.data:
            daysStr += day + ','
        professor = Professor.query.filter_by(name = form.prof.data).first()
        course = Course(course = form.course.data , type=form.type.data , company=form.company.data ,
        hours=form.hours.data , professor=professor.id , book=form.book.data ,
        place=form.place.data , price=form.price.data , start=form.start.data , end=form.end.data,
        comment=form.comment.data , weekly=form.weekly.data , days=daysStr , hoursPerSession=form.hoursPerSession.data)
        if len(form.days.data) != form.weekly.data:
            flash('Error in days selection' , 'danger')
            return redirect(url_for('addCourse'))
        db.session.add(course)
        db.session.commit()
        if form.po.data:
            form.po.data.save(app.root_path , 'static/pos/' , course.company+'.pdf')
        flash('Course added successfully' , 'success')
        return redirect(url_for('overview'))
    return render_template('addCourse.html' , form=form , modify=False)


def getCourseStudents(course_id):
    course = Course.query.filter_by(id=course_id).first()

    rooms = Room.query.filter_by(courseId=course_id).all()
    db.session.commit()

    studentsIds = [room.studentId for room in rooms]

    students = []

    for studentId in studentsIds:
        s = Student.query.filter_by(id=studentId).first()
        students.append(s)

    return students


@app.route('/course/<int:course_id>' , methods=['GET' , 'POST'])
def courseDetails(course_id):

    course = Course.query.filter_by(id=course_id).first()

    rooms = Room.query.filter_by(courseId=course_id).all()
    db.session.commit()

    over = False
    checked = course.checked
    if datetime.datetime.today() > course.end:
        over = True

    courseName = course.course
    students = []

    studentsIds = [room.studentId for room in rooms]

    for studentId in studentsIds:
        s = Student.query.filter_by(id=studentId).first()
        students.append(s)

    return render_template('course.html' , students=students , name = courseName ,
     course_id=course_id , over=over , checked=checked)


@app.route('/certifs/<int:cid>')
def prepareCertifs(cid):

    print('preparing ')
    document = Doc('certifs.docx')
    course = Course.query.filter_by(id=cid).first()

    students = getCourseStudents(cid)

    for student in students:
        name = student.fullName.replace(' ','')
        document.replace('Mohamed Redissi' , student.fullName)
        document.replace('Business English' , course.course)
        document.replace('Business 1' , '')
        document.replace('22.10.2018' , str(course.start.strftime('%d.%m.%y')))
        document.replace('12.02.2019' , str(course.end.strftime('%d.%m.%y')))
        try :
            os.mkdir(app.root_path + '/certifs/' + course.company)
        except :
            pass
        document.saveDoc('certifs/' + course.company + '/' + name + '.docx')

    return redirect(url_for('courseDetails' , course_id=cid))

@app.route('/removeStudentFromCourse/<int:sid>/<int:cid>')
def removeStudentFromCourse(sid,cid):
    room = Room.query.filter_by(studentId=sid).filter_by(courseId=cid).first()

    db.session.delete(room)
    db.session.commit()

    return redirect(url_for('courseDetails' , course_id=cid))


@app.route('/delete/<int:courseid>')
def delete(courseid):
    course = Course.query.filter_by(id=courseid).first()
    rooms = Room.query.filter_by(courseId=courseid).all()

    for room in rooms:
        db.session.delete(room)

    db.session.delete(course)

    db.session.commit()

    return redirect(url_for('courses'))

@app.route('/PO/<int:courseid>')
def PurchaseOrder(courseid):
    course = Course.query.filter_by(id=courseid).first()

    return render_template('po.html' , course=course)


@app.route('/finished/<int:courseid>' , methods=['GET' , 'POST'])
def validateCourse(courseid):
    studentsIds = request.args.getlist('key[]')
    for s in studentsIds:
        room = Room.query.filter_by(courseId=courseid,studentId=s).first()
        room.status = True
        db.session.commit()
    course = Course.query.filter_by(id=courseid).first()
    course.checked = True
    db.session.commit()
    return redirect(url_for('courseDetails' , course_id=courseid))

@app.route('/results/<int:courseid>')
def results(courseid):
    rooms = Room.query.filter_by(courseId=courseid).all()
    course = Course.query.filter_by(id=courseid).first()
    db.session.commit()
    students = []

    for room in rooms:
        s = Student.query.filter_by(id=room.studentId).first()
        students.append({'student' : s.fullName , 'passed' : room.status})
        db.session.commit()

    db.session.commit()

    return render_template('results.html' , students=students , course=course)


@app.route('/modifyCourse/<int:courseid>' , methods=['GET' , 'POST'])
def courseModify(courseid):
    course = Course.query.filter_by(id=courseid).first()
    form = addCourseForm()
    if form.validate_on_submit():
        daysStr = ''
        for day in form.days.data:
            daysStr += day + ','
        professor = Professor.query.filter_by(name = form.prof.data).first()
        course.course = form.course.data
        course.type = form.type.data
        course.company = form.company.data
        course.hours=form.hours.data
        course.professor=professor.id
        course.book=form.book.data
        course.place=form.place.data
        course.price=form.price.data
        course.start=form.start.data
        course.end=form.end.data
        course.comment=form.comment.data
        course.weekly=form.weekly.data
        course.days=daysStr
        course.hoursPerSession = form.hoursPerSession.data
        if len(form.days.data) != form.weekly.data:
            flash('Error in days selection','danger')
            return redirect(url_for('addCourse'))
        db.session.commit()
        if form.po.data:
            name = course.company+'.pdf'
            form.po.data.save(os.path.join(app.root_path + '/static/pos/' , name ))
        flash('Course Modified successfully' , 'success')
        redirect(url_for('courseDetails' , course_id=courseid))
    return render_template('addCourse.html' , form = form , modify=True , course=course)
