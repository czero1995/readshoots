from . import admin
from flask import render_template,flash,redirect,url_for,session,request
from app.admin.forms import LoginForm,TagForm,ImageForm,BannerForm
from app.models import Admin,Tag,Image,Banner,User,Comment,Collect
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


@admin.route("/tag/list/<int:page>/",methods=["GET"])
def tag_list(page=None):
    if page is None:
        page = 1
    page_data = Tag.query.order_by(
        Tag.addtime.desc()
    ).paginate(page=page,per_page=3)
    return render_template("admin/tag_list.html",page_data=page_data)



@admin.route("/tag/del/<int:id>/",methods=["GET"])
def tag_del(id=None):
    tag = Tag.query.filter_by(id=id).first_or_404()
    db.session.delete(tag)
    db.session.commit()
    flash("删除标签成功","ok")
    return redirect(url_for('admin.tag_list',page=1))

@admin.route("/tag/edit/<int:id>/",methods=["GET","POST"])
def tag_edit(id=None):
    form = TagForm()
    tag = Tag.query.get_or_404(id)
    if form.validate_on_submit():
        data = form.data
        tag_count = Tag.query.filter_by(name=data["name"]).count()
        if tag.name != data["name"] and tag_count == 1:
            flash("标签名称已经存在" ,"err")
            return redirect(url_for('admin.tag_edit',id=id))
        tag.name = data["name"]
        db.session.add(tag)
        db.session.commit()
        flash("修改标签成功","ok")
        redirect(url_for('admin.tag_edit',id=id))
    return render_template("admin/tag_edit.html",form=form,tag=tag)


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

@admin.route("/image/list/<int:page>/",methods=["GET"])
def image_list(page=None):
    if page is None:
        page = 1
    page_data = Image.query.join(Tag).filter(
        Tag.id == Image.tag_id
    ).order_by(
        Image.addtime.desc()
    ).paginate(page=page, per_page=3)
    return render_template("admin/image_list.html",page_data=page_data)

@admin.route("/image/del/<int:id>/",methods=["GET"])

def image_del(id=None):
    image = Image.query.get_or_404(int(id))
    db.session.delete(image)
    db.session.commit()
    flash("删除图片成功","ok")
    return redirect(url_for('admin.image_list',page=1))

@admin.route("/image/edit/<int:id>/",methods=["GET","POST"])
def image_edit(id=None):
    form = ImageForm()
    image = Image.query.get_or_404(int(id))
    if request.method == 'GET':
        form.info.data = image.info
        form.tag_id.data = image.tag_id
    if form.validate_on_submit():
        data = form.data
        if not os.path.exists(app.config["UP_DIR"]):
            os.makedirs(app.config["UP_DIR"])
            os.chmod(app.config["UP_DIR"], "rw")
        if form.img.data.filename != "":
            file_logo = secure_filename(form.img.data.filename)
            image.img = change_filename(file_logo)
            form.img.data.save(app.config["UP_DIR"] + image.img)

        image.tag_id = data["tag_id"]
        image.info = data["info"]
        image.title = data["title"]
        db.session.add(image)
        db.session.commit()
        flash("图片编辑成功","ok")
        return redirect(url_for('admin.image_edit',id = image.id))
    return render_template("admin/image_edit.html",form=form,image = image)

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

@admin.route("/user/list/<int:page>",methods=["GET"])
def user_list(page = None):
    if page is None:
        page = 1
    page_data = User.query.order_by(
        User.addtime.desc()
    ).paginate(page=page,per_page=10)
    return render_template("admin/user_list.html",page_data=page_data)

@admin.route("/user/view/<int:id>/",methods=["GET"])
def user_view(id = None):
    user = User.query.get_or_404(int(id))
    return render_template("admin/user_view.html",user=user)

@admin.route("/user/del/<int:id>/",methods=["GET"])
def user_del(id = None):
    user = User.query.get_or_404(int(id))
    db.session.delete(user)
    db.session.commit()
    flash("删除会员成功 ","ok")
    return redirect(url_for("admin.user_list",page=1))

@admin.route("/commemt/list/<int:page>",methods=["GET"])
def comment_list(page = None):
    if page is None:
        page = 1
    page_data = Comment.query.join(
        Image
    ).join(
        User
    ).filter(
         Image.id == Comment.image_id,
         User.id == Comment.user_id,
    ).order_by(
        Comment.addtime.desc()
    ).paginate(page=page,per_page=10)
    return render_template("admin/comment_list.html",page_data=page_data)

@admin.route("/comment/del/<int:id>/",methods=["GET"])
def comment_del(id = None):
    comment = Comment.query.get_or_404(int(id))
    db.session.delete(comment)
    db.session.commit()
    flash("删除评论成功 ","ok")
    return redirect(url_for("admin.comment_list",page=1))

@admin.route("/collect/list/<int:page>",methods=["GET"])
def collect_list(page = None):
    if page is None:
        page = 1
    page_data = Collect.query.join(
        Image
    ).join(
        User
    ).filter(
         Image.id == Collect.image_id,
         User.id == Collect.user_id,
    ).order_by(
        Collect.addtime.desc()
    ).paginate(page=page,per_page=10)
    return render_template("admin/collect_list.html",page_data=page_data)

@admin.route("/collect/del/<int:id>/",methods=["GET"])
def collect_del(id = None):
    collect =  Collect.query.get_or_404(int(id))
    db.session.delete(collect)
    db.session.commit()
    flash("删除收藏成功 ","ok")
    return redirect(url_for("admin.collect_list",page=1))