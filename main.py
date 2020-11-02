import pandas as pd
import sqlite3
from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from forms import RegistrationForm, LoginForm, PostForm
import datetime
from flask_login import LoginManager, UserMixin, login_user, current_user
from flask_login import logout_user, login_required
from flask_bootstrap import Bootstrap

from forms import RegistrationForm, LoginForm, PostForm

# initialize the app with all needed attributes

app = Flask(__name__)

# in order to use some bootstrap building blocks easier
Bootstrap(app)
# for passwords to be en- and decrypted
bcrypt = Bcrypt(app)
# for login management
login_manager = LoginManager(app)
login_manager.login_view = "login"


###############################################################################
# SQL DATABASE CONFIGURATION
###############################################################################

app.config["SECRET_KEY"] = "secret-key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
# initialize the database
db = SQLAlchemy(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

# create User and Post class with respective columns


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(60), nullable=False)
    last_name = db.Column(db.String(60), nullable=False)
    user_handle = db.Column(db.String(60), unique=True, nullable=False)
    # email is unique
    email = db.Column(db.String(100), unique=True, nullable=False)
    # password is unique
    password = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=True)


def __repr__(self):
    # string printed if we call print function on an instance of this object
    return f"User(id: '{self.id}', " +\
        f" first_name: '{self.first_name}', " +\
        f" last_name: '{self.last_name}', " +\
        f" user_handle: '{self.user_handle}', " +\
        f" email: '{self.email}', " +\
        f" password: '{self.password}', " +\
        f" description: '{self.description}')"


class Post(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_handle = db.Column(db.String(60), unique=True, nullable=False)
    post_content = db.Column(db.String(140), nullable=False)
    post_length = db.Column(db.Integer, nullable=False)
    post_time = db.Column(db.DateTime, nullable=True,
                          default=datetime.datetime.now)
    # foreign key to user class
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)


def __repr__(self):
    return f"Product(id: '{self.id}', user_handle: '{self.user_handle}',post_content: '{self.post_content}', post_length: '{self.post_length}', post_time: '{self.post_time}', user_url: '{self.user_url}', user_id: '{self.user_id}')"


###############################################################################
# ROUTES
###############################################################################


@ app.route("/homepage")
@ login_required
def homepage():
    df_post = pd.read_sql(Post.query.statement, db.session.bind)
    return render_template("homepage.html", new_df=df_post)


@ app.route("/register", methods=["GET", "POST"])
def register():

    if current_user.is_authenticated:
        return redirect(url_for("login"))

    form = RegistrationForm()

    if form.validate_on_submit():
        registration_worked = register_user(form)
        if registration_worked:
            return redirect(url_for("login"))

    return render_template("register.html", form=form)


@ app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("homepage"))

    form = LoginForm()

    if form.validate_on_submit():
        if is_login_successful(form):
            return redirect(url_for("homepage"))
        else:
            if email_already_taken(form):
                return redirect(url_for("login"))
            else:
                return redirect(url_for("register"))

    return render_template("login.html", form=form)


@ app.route("/upload", methods=["GET", "POST"])
@ login_required
def upload():
    form = PostForm()

    if form.validate_on_submit():
        add_post(form)
        return redirect(url_for("homepage"))

    return render_template("upload.html", form=form)


@ app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("login"))


@ app.route("/profile/<user_handle>")
@ login_required
def profile(user_handle):
    if get_profile(user_handle) is False:
        return redirect(url_for("homepage"))

    first_name, last_name = get_profile(user_handle)
    return render_template("profile.html",
                           user_handle=user_handle,
                           first_name=first_name,
                           last_name=last_name)


###############################################################################
# SUPPORTING FUNCTIONS
###############################################################################


def register_user(form_data):

    def email_already_taken(email):
        if User.query.filter_by(email=email).count() > 0:
            return True
        else:
            return False

    if email_already_taken(form_data.email.data):
        return False

    hashed_password = bcrypt.generate_password_hash(form_data.password.data)

    user = User(first_name=form_data.first_name.data,
                last_name=form_data.last_name.data,
                user_handle=form_data.user_handle.data,
                email=form_data.email.data,
                password=hashed_password,
                description=form_data.description.data)

    db.session.add(user)

    db.session.commit()

    return True


def email_already_taken(form_data):
    email = form_data.email.data
    if User.query.filter_by(email=email).count() > 0:
        return True
    else:
        return False


def is_login_successful(form_data):

    email = form_data.email.data
    password = form_data.password.data

    user = User.query.filter_by(email=email).first()

    if user is not None:
        if bcrypt.check_password_hash(user.password, password):
            login_user(user)

            return True

    return False


def measure_length(form_data):
    post_content = form_data.post_content.data
    post_content_length = Post.query.filter_by(post_content=post_content).first()
    if post_content:
        post_length = len(post_content)
        return post_length


def add_post(form_data):
    post_content = form_data.post_content.data
    post_length = len(post_content)
    if post_length < 140:
        post = Post(post_content=form_data.post_content.data, post_length=post_length,
                    user_id=current_user.id, user_handle="/profile/" + str(current_user.user_handle))

        db.session.add(post)

        db.session.commit()


def get_profile(url_handle):
    user_handle = url_handle
    user = User.query.filter_by(user_handle=user_handle).first()
    if user is None:
        return False
    else:
        first_name = user.first_name
        last_name = user.last_name
        return first_name, last_name


if __name__ == "__main__":
    app.run(debug=True)
