from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, BooleanField, SubmitField 
from wtforms import TextAreaField, FileField, DecimalField, IntegerField, SelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length, NumberRange

class AddCourseForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(),Length(min=4, max=100)])
    summary = TextAreaField('Summary', validators=[DataRequired(), Length(min=100, max=5000)])
    image = FileField('Add image', validators=[FileAllowed(['jpg', 'png'])])
    price = DecimalField('Price', default=99.99)
    category_id = SelectField('Select category', coerce=int)
    submit = SubmitField('Add course')

class EditCourseForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(),Length(min=4, max=100)])
    summary = TextAreaField('Summary', validators=[DataRequired(), Length(min=100, max=5000)])
    image = FileField(
        'Update course image',
        validators=[
            FileAllowed(['jpg', 'png'], 'Images only with extension .jpg or .png')
        ]
    )
    price = DecimalField('Price', default=1.99)
    category_id = SelectField('Category', coerce=int)
    update = SubmitField('Update')
    cancel = SubmitField('Cancel')

class ReviewForm(FlaskForm):
    rating = DecimalField(default=0.0, validators=[NumberRange(min=0, max=5)])
    text = TextAreaField('Write a review')
    submit = SubmitField('Submit')

class CategoryForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(),Length(min=2, max=22)])
    submit = SubmitField('Submit')

class EditCategoryForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(),Length(min=2, max=22)])
    update = SubmitField('Update')
    cancel = SubmitField('Cancel')