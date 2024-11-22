from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, EqualTo

# Registration Form
class RegistrationForm(FlaskForm):
    email = StringField(
        'Email',
        validators=[
            DataRequired(),
            Email(message='Invalid email address.'),
            Length(max=120)
        ]
    )
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(),
            Length(min=6, message='Password must be at least 6 characters long.')
        ]
    )
    confirm_password = PasswordField(
        'Confirm Password',
        validators=[
            DataRequired(),
            EqualTo('password', message='Passwords must match.')
        ]
    )
    user_type = SelectField(
        'I am a:',
        choices=[('Candidate', 'Candidate'), ('Company', 'Company')],
        validators=[DataRequired()]
    )
    submit = SubmitField('Register')

# Login Form
class LoginForm(FlaskForm):
    email = StringField(
        'Email',
        validators=[
            DataRequired(),
            Email(message='Invalid email address.')
        ]
    )
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

# Job Posting Form
class PostJobForm(FlaskForm):
    title = StringField(
        'Job Title',
        validators=[
            DataRequired(),
            Length(max=100, message='Job title must be under 100 characters.')
        ]
    )
    description = TextAreaField(
        'Job Description',
        validators=[
            DataRequired(),
            Length(min=10, message='Description must be at least 10 characters long.')
        ]
    )
    submit = SubmitField('Post Job')

# Profile Form (Optional for Candidate Profile Creation)
class ProfileForm(FlaskForm):
    name = StringField(
        'Full Name',
        validators=[
            DataRequired(),
            Length(max=100)
        ]
    )
    skills = TextAreaField(
        'Skills (comma-separated)',
        validators=[
            DataRequired(),
            Length(min=5, message='Please add at least one skill.')
        ]
    )
    submit = SubmitField('Update Profile')

# Apply Job Form
class ApplyJobForm(FlaskForm):
    submit = SubmitField('Apply', validators=[DataRequired()])
