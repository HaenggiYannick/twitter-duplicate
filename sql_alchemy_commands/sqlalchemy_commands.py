from flask_login import LoginManager, UserMixin, login_user, current_user, logout_user, login_required
from main import db, User, Post
from main import db
from main import User, Post
import pandas as pd
import datetime
from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, current_user
from flask_login import logout_user, login_required
from forms import RegistrationForm, LoginForm, PostForm


# create the database
db.create_all()
# first check of database content
all_users = User.query.all()
print(all_users)


# enter some content to the database

# add first User
user1 = User(first_name="Yannick",
             last_name="Haenggi",
             user_handle="yannickhaenggi",
             email="yannick.haenggi@unisg.ch",
             password="password",
             description="""I'm the first user of this Application""")
db.session.add(user1)
# commit session
db.session.commit()
# add post
post1 = Post(post_content="I am the first user of this awesome Twitter duplicate",
             post_length=53,
             post_time=datetime.datetime.now(),
             user_id=1)
db.session.add_all([user1, post1])
# commit session
db.session.commit()
# check whether both sessions were entered correctly
print(user1)
print(post1)


# different commands for querying the sql database


# all contents
all_posts = Post.query.all()
all_posts
# querying for the first user (ID = 1)
my_post = Post.query.get(1)
my_post
# querying for post with length 53
my_post = Post.query.filter_by(post_length=53).first()
my_post
# first user
my_user = User.query.first()
my_user
# entire content of User class respectively Post class as dataframe
df_post = pd.read_sql(Post.query.statement, db.session.bind)
df_post
df_user = pd.read_sql(User.query.statement, db.session.bind)
df_user


# command whenever an error happens


# reset current session
db.session.rollback()
