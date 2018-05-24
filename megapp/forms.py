from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SelectField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from megapp.models import User

class UpdateForm(FlaskForm):
    updated = SelectField('Update', validators=[DataRequired()])
    
    #def __init__(self, *args, **kwargs):
    #    super().__init__(*args, **kwargs)
    #    self.items.choices = []

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()]) #DR():notEmpty
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')
