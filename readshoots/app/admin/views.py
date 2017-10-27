from . import admin
from flask import render_template,flash,redirect,url_for,session,request
from app.admin.forms import LoginForm,TagForm,ImageForm,BannerForm
from app.models import Admin,Tag,Image,Banner
from app import db,app
from werkzeug.utils import secure_filename
import os,datetime,uuid

#修改文件名称
def change_filename(filename):
    fileinfo = os.path.splitext(filename)
    filename = datetime.datetime.now().strftime("%Y%m%d%H%M%S")+str(uuid.uuid4().hex)+fileinfo[-1]
    return filename

@admin.route("/")
def index():
    return render_template("admin/index.html")


@admin.route("/login/",methods=["GET","POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        data = form.data
        admin = Admin.query.filter_by(name=data["account"]).first()
        if not admin.check_pwd(data["pwd"]):
            flash("密码错误","err")
            return redirect(url_for("admin.login"))
        session["admin"] = data["account"]
        session["admin_id"] = admin.id
        return redirect(request.args.get("next") or url_for("admin.index"))
    return render_template("admin/login.html",form=form)


@admin.route("/tag/add/",methods=["GET","POST"])
# @admin_auth
def tag_add():
    form = TagForm()
    if form.validate_on_submit():
        data = form.data
        tag = Tag.query.filter_by(name=data["name"]).count()
        if tag == 1:
            flash("标签名称已经存在" ,"err")
            return redirect(url_for('admin.tag_add'))
        tag = Tag(
            name = data["name"]
        )
        db.session.add(tag)
        db.session.commit()
        flash("添加标签成功","ok")
        redirect(url_for('admin.tag_add'))
    return render_template("admin/tag_add.html",form=form)


@admin.route("/image/add/",methods=["GET","POST"])
def image_add():
    form = ImageForm()
    if form.validate_on_submit():
        data = form.data
        file_img = secure_filename(form.img.data.filename)
        if not os.path.exists(app.config["UP_DIR"]):
            os.makedirs(app.config["UP_DIR"])
            os.chmod(app.config["UP_DIR"],"rw")
        img = change_filename(file_img)
        form.img.data.save(app.config["UP_DIR"]+img)
        image = Image(
            title = data["title"],
            info=data["info"],
            img = img,
            playnum=0,
            commentnum=0,
            tag_id=int(data["tag_id"]),
        )
        db.session.add(image)
        db.session.commit()
        flash("图片添加成功","ok")
        return redirect(url_for('admin.image_add'))
    return render_template("admin/image_add.html",form=form)

@admin.route("/banner/add/",methods=["GET","POST"])
def banner_add():
    form = BannerForm()
    if form.validate_on_submit():
        data = form.data
        file_img = secure_filename(form.img.data.filename)
        if not os.path.exists(app.config["UP_DIR"]):
            os.makedirs(app.config["UP_DIR"])
            os.chmod(app.config["UP_DIR"],"rw")
        img = change_filename(file_img)
        form.img.data.save(app.config["UP_DIR"]+img)
        banner = Banner(
            title = data["title"],
            info=data["info"],
            img = img,
        )
        db.session.add(banner)
        db.session.commit()
        flash("图片添加成功","ok")
        return redirect(url_for('admin.banner_add'))
    return render_template("admin/banner_add.html",form=form)