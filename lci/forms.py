from flask_wtf import FlaskForm
from wtforms import SelectMultipleField, StringField, PasswordField, SubmitField, BooleanField,FloatField, TextAreaField, IntegerField, DateField, FileField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, NumberRange


class addCourseForm(FlaskForm):
    course = StringField('Course', validators=[DataRequired(), Length(min=2, max=50)])

    type = StringField('Type', validators=[DataRequired(), Length(min=2, max=20)])

    company = StringField('Company', validators=[DataRequired(), Length(min=2, max=20)])

    hours = IntegerField('Hours', validators=[DataRequired()])

    prof = StringField('Professor', validators=[DataRequired()])

    book = StringField('Book', validators=[DataRequired(), Length(min=2, max=20)])

    place = StringField('Place', validators=[DataRequired(), Length(min=2, max=20)])

    price = StringField('Price', validators=[DataRequired(), Length(min=2, max=20)])

    start = DateField('Start date' , format='%d/%m/%Y' , validators=[DataRequired()])

    end = DateField('End date' , format='%d/%m/%Y' , validators=[DataRequired()])

    po = FileField('PO')

    comment = TextAreaField('Comment', validators=[DataRequired(), Length(min=2, max=20)])

    weekly = IntegerField('Sessions per week', validators=[DataRequired() , NumberRange(1,7)])

    days = SelectMultipleField('Days',  choices= [('1','Monday'),('2','Tuesday'),('3','Wednesday'),
    ('4','Thursday'),('5','Friday'),('6','Saturday'),('7','Sunday')] ,validators=[DataRequired()])

    hoursPerSession = FloatField('Hours Per Session' , validators=[DataRequired()])

    submit = SubmitField('Add Course')

class addProfForm(FlaskForm):

    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=30)])

    email = StringField('Email', validators=[DataRequired(), Email()])

    phone = StringField('Phone', validators=[DataRequired(), Length(min=2, max=20)])

    submit = SubmitField('Submit')


class ModifyProfForm(FlaskForm):

    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=30)])

    email = StringField('Email', validators=[DataRequired(), Email()])

    phone = StringField('Phone', validators=[DataRequired(), Length(min=2, max=20)])

    recapHours = IntegerField('Recap Hours', validators=[DataRequired()])

    submit = SubmitField('Submit')



class addStudentForm(FlaskForm):

    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=20)])

    email = StringField('Email', validators=[DataRequired(), Email()] , default='none@none.none')

    phone = StringField('Phone', validators=[DataRequired(), Length(min=2, max=20)] , default='none@none.none')

    submit = SubmitField('Add Student')
