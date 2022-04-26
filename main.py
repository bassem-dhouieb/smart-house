import requests
from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditor, CKEditorField
import os
from flask import request
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")
ckeditor = CKEditor(app)
Bootstrap(app)

##CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL", 'sqlite:///posts.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
from datetime import datetime


##CONFIGURE TABLE
class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    subtitle = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(250), nullable=False)
    body = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    img_url = db.Column(db.String(250), nullable=False)


##WTForm
class CreatePostForm(FlaskForm):
    title = StringField("Blog Post Title", validators=[DataRequired()])
    subtitle = StringField("Subtitle", validators=[DataRequired()])
    author = StringField("Your Name", validators=[DataRequired()])
    img_url = StringField("Blog Image URL", validators=[DataRequired(), URL()])
    body = CKEditorField("Blog Content", validators=[DataRequired()])
    submit = SubmitField("Submit Post")


db.create_all()


##RENDER HOME PAGE USING DB
@app.route('/')
def get_all_posts():
    posts = BlogPost.query.all()
    return render_template("index.html", all_posts=posts)


##RENDER POST USING DB
@app.route("/post/<int:index>")
def show_post(index):
    requested_post = BlogPost.query.get(index)
    return render_template("post.html", post=requested_post)


@app.route("/new-post", methods=["GET", "POST"])
def add_new_post():
    form = CreatePostForm()

    new_post = BlogPost(
        title=request.args.get('title')+" visits you at "+datetime.now().strftime(" %H:%M:%S , %m/%d/%Y"),
        subtitle=request.args.get('title'),
        body=request.args.get('title'),
        img_url=request.args.get('img'),
        author=request.args.get('title'),
        date=datetime.now().strftime(" %H:%M:%S , %m/%d/%Y")

    )

    db.session.add(new_post)
    db.session.commit()
    return redirect(url_for('get_all_posts'))


@app.route("/edit-post/<int:post_id>", methods=["GET", "POST"])
def edit_post(post_id):
    post = BlogPost.query.get(post_id)
    edit_form = CreatePostForm()
    edit_form.title.data = post.title
    edit_form.subtitle.data = post.subtitle
    edit_form.body.data = post.body
    edit_form.img_url.data = post.img_url
    edit_form.author.data = post.author
    edit_date = datetime.now().strftime(" %H:%M:%S , %m/%d/%Y")
    return render_template("make-post.html", form=edit_form, is_edit=True)


@app.route("/delete/<int:post_id>")
def delete_post(post_id):
    post_to_delete = BlogPost.query.get(post_id)
    db.session.delete(post_to_delete)
    db.session.commit()
    return redirect(url_for('get_all_posts'))


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/control")
def contact():
    return render_template("control.html")

@app.route("/door1")
def door1():
    result = requests.get("https://apii-sys.herokuapp.com/api").json()[0]
    result["port1"] = not result["port1"]
    requests.patch("https://apii-sys.herokuapp.com/api/action",json=result)
    return render_template("control.html")

@app.route("/door2")
def door2():
    result = requests.get("https://apii-sys.herokuapp.com/api").json()[0]
    result["port2"] = not result["port2"]
    requests.patch("https://apii-sys.herokuapp.com/api/action",json=result)
    return render_template("control.html")

@app.route("/door3")
def door3():
    result = requests.get("https://apii-sys.herokuapp.com/api").json()[0]
    result["port3"] = not result["port3"]
    requests.patch("https://apii-sys.herokuapp.com/api/action",json=result)
    return render_template("control.html")

@app.route("/light")
def light():
    result = requests.get("https://apii-sys.herokuapp.com/api").json()[0]
    result["lumiere"] = not result["lumiere"]
    requests.patch("https://apii-sys.herokuapp.com/api/action",json=result)
    return render_template("control.html")

@app.route("/air-conditioner")
def conditioner():
    result = requests.get("https://apii-sys.herokuapp.com/api").json()[0]
    result["climatiseur"] = not result["climatiseur"]
    requests.patch("https://apii-sys.herokuapp.com/api/action",json=result)
    return render_template("control.html")

@app.route("/heater")
def heater():
    result = requests.get("https://apii-sys.herokuapp.com/api").json()[0]
    result["chauffage"] = not result["chauffage"]
    requests.patch("https://apii-sys.herokuapp.com/api/action",json=result)
    return render_template("control.html")


if __name__ == "__main__":
    app.run(debug=True, port=8000)
