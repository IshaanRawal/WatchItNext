# This segment of code uses inbuilt libraries to validate if a certain form has been submitted by the user.
# It also checks wether the entered email id is valid or if the passwords given during registeration match.

from ast import Str
from wsgiref.validate import validator
from xml.dom import ValidationErr
from flask import Flask
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from Recommendation.model import user
from Recommendation import bcrypt
class RegisterForm(FlaskForm):

    def validate_username(self, username_to_check):
        User = user.query.filter_by(username=username_to_check.data).first()
        if User: 
            raise ValidationError('Username already exists! Please try a different username')


    def validate_email_address(self, email_address_to_check):
        email_address = user.query.filter_by(email_address=email_address_to_check.data).first()
        if email_address:
            raise ValidationError('Email Address alrerady exists! Please try a different email address')

    username = StringField(label='User Name: ', validators=[Length(min=2, max=30), DataRequired()])
    email_address = StringField(label='Email Address: ', validators=[Email(),DataRequired()])
    password1 =     PasswordField(label='Password',validators=[Length(min=6),DataRequired()])
    password2 =     PasswordField(label='Confirm Password', validators=[EqualTo('password1'),DataRequired()]) 
    submit = SubmitField(label='Create Account')

class LoginForm(FlaskForm):

    username = StringField(label='User Name: ', validators=[DataRequired()])
    password = PasswordField(label='Password: ', validators=[DataRequired()])
    submit = SubmitField(label='Sign In')

class SearchForm(FlaskForm):
    movie_name = StringField(label='Search Your Movie: ', validators=[DataRequired()])
    search = SubmitField(label='Search')