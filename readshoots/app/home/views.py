from . import home
from flask import render_template,flash,redirect,url_for,session
from app import db,app
from werkzeug.security import generate_password_hash
from app.home.forms import RegisterForm,LoginForm,UserDetailForm,PwdForm
from app.models import User,Image,Tag,Banner
import os
@home.route("/")
def readshoot():
    banner = Banner.query.all()
    people = Image.query.join(
        Tag
    ).filter(
        Tag.name == 'people'
    )
    city = Image.query.join(
        Tag
    ).filter(
        Tag.name == 'city'
    )
    return render_template('home/index.html',people=people,city=city,banner=banner)

@home.route("/index/")
def index():
    people = Image.query.join(
        Tag
    ).filter(
        Tag.name == 'people'
    )
    city = Image.query.join(
        Tag
    ).filter(
        Tag.name == 'city'
    )
    return render_template('home/index.html',people=people,city=city)

@home.route("/login/",methods=["GET","POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        data = form.data
        user = User.query.filter_by(name=data["name"]).first()
        if not user.check_pwd(data["pwd"]):
            flash("密码错误","err")
            return redirect(url_for("home.login"))
        session["user"] = user.name
        session["user_id"] = user.id
        return redirect(url_for("home.index"))
    return render_template('home/login.html',form=form)


@home.route("/register/",methods=["GET","POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        data = form.data
        user = User(
            name = data["name"],
            email = data["email"],
            phone=data["phone"],
            pwd=generate_password_hash(data["pwd"]),

        )
        db.session.add(user)
        db.session.commit()
        flash("注册成功","ok")
    return render_template('home/register.html',form = form)

@home.route("/logout/")
def logout():
    session.pop("user",None)
    session.pop("user_id",None)
    return redirect(url_for("home.login"))

@home.route("/user/")
def user():
    form = UserDetailForm()
    user = User.query.get(int(session['user_id']))
    return render_template("home/user.html",form=form,user=user)


@home.route("/pwd/", methods=["GET","POST"])
def pwd():
    form = PwdForm()
    if form.validate_on_submit():
        data = form.data
        user = User.query.filter_by(name=session["user"]).first()
        if not user.check_pwd(data["old_pwd"]):
            flash("旧密码出错", "err")
            return redirect(url_for('home.pwd'))
        user.pwd = generate_password_hash(data["new_pwd"])
        db.session.add(user)
        db.session.commit()
        flash("修改密码成功，请重新登录","ok")
        return redirect(url_for('home.logout'))
    return render_template("home/pwd.html",form=form)