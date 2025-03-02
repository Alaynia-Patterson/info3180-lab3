from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email

class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(message="Please enter your full name.")])
    email = StringField('E-mail', validators=[DataRequired(message="Please enter your e-mail address."), Email()])
    subject = StringField('Subject', validators=[DataRequired(message="Please enter the subject for your message.")])
    message = TextAreaField('Message', validators=[DataRequired(message="Please enter the message you would like to send.")])
    submit = SubmitField('Send')