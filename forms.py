from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField, PasswordField, DateTimeField
from wtforms.validators import DataRequired


class RegistrationForm(FlaskForm):
    first_name = StringField("first_name", validators=[DataRequired()])
    last_name = StringField("last_name", validators=[DataRequired()])
    user_handle = StringField("user_handle", validators=[DataRequired()])
    email = StringField("email", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired()])
    description = StringField("description", validators=[DataRequired()])
    submit_button = SubmitField("Submit")


class LoginForm(FlaskForm):
    email = StringField("email", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired()])
    submit_button = SubmitField("Submit")


class PostForm(FlaskForm):
    post_content = StringField("Post Content", validators=[DataRequired()])
    submit_button = SubmitField("Submit")


"""post_length = StringField("Post Length", validators=[DataRequired()])
post_time = DateTimeField("Time of your Post", validators=[DataRequired()])"""
