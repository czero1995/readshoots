from . import home
from flask import render_template,flash,redirect,url_for,session,request
from app import db,app
from werkzeug.security import generate_password_hash
from app.home.forms import RegisterForm,LoginForm,UserDetailForm,PwdForm,CommentForm
from app.models import User,Image,Tag,Banner,Collect,Comment
import os,datetime,uuid
from werkzeug.utils import secure_filename
#修改文件名称
def change_filename(filename):
    fileinfo = os.path.splitext(filename)
    filename = datetime.datetime.now().strftime("%Y%m%d%H%M%S")+str(uuid.uuid4().hex)+fileinfo[-1]
    return filename
@home.route("/")
def readshoot():
    image = Image.query.all()
    chooice =[(v.id) for v in image];
    print(chooice)
    user = User.query.all()
    banner = Banner.query.all()
    people = Image.query.join(
        Tag
    ).filter(
        Tag.name == 'people'
    )
    landscapes = Image.query.join(
        Tag
    ).filter(
        Tag.name == 'landscapes'
    )
    nature = Image.query.join(
        Tag
    ).filter(
        Tag.name == 'nature'
    )
    city = Image.query.join(
        Tag
    ).filter(
        Tag.name == 'city'
    )
    animals = Image.query.join(
        Tag
    ).filter(
        Tag.name == 'animals'
    )
    return render_template('home/index.html',chooice=chooice,people=people,landscapes=landscapes,nature=nature,city=city,animals=animals,user=user)

@home.route("/discover")
def discover():
    hot = Image.query.order_by(
        Image.playnum.desc()
    )
    new = Image.query.order_by(
        Image.addtime.desc()
    )
    max = Image.query.order_by(
        Image.commentnum.desc()
    )

    return render_template('home/discover.html',hot=hot,new=new,max=max);

@home.route("/index/")
def index():
    user = User.query.all()
    people = Image.query.join(
        Tag
    ).filter(
        Tag.name == 'people'
    )
    landscapes = Image.query.join(
        Tag
    ).filter(
        Tag.name == 'landscapes'
    )
    nature = Image.query.join(
        Tag
    ).filter(
        Tag.name == 'nature'
    )
    city = Image.query.join(
        Tag
    ).filter(
        Tag.name == 'city'
    )
    animals = Image.query.join(
        Tag
    ).filter(
        Tag.name == 'animals'
    )
    return render_template('home/index.html',people=people,landscapes=landscapes,nature=nature,city=city,animals=animals)

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

# 会员信息界面
@home.route('/user/', methods=['GET', 'POST'])
def user():
    form = UserDetailForm()
    user = User.query.get(int(session['user_id']))
    form.face.validators = []
    if request.method == 'GET':
        form.name.data = user.name
        form.email.data = user.email
        form.phone.data = user.phone
        form.info.data = user.info
    if form.validate_on_submit():
        data = form.data
        file_face = secure_filename(form.face.data.filename)  # secure_filename函数来操作安全文件名
        # 判断上传文件的文件夹是否存在
        if not os.path.exists(app.config["FC_DIR"]):
            os.makedirs(app.config["FC_DIR"])  # 如果不存在 就创建一个文件夹
            os.chmod(app.config["FC_DIR"], "rw")  # 给一个可读可写的权限
        user.face = change_filename(file_face)  # 修改文件名
        form.face.data.save(app.config["FC_DIR"] + user.face)  # 保存文件

        name_count = User.query.filter_by(name=data['name']).count()
        if data['name'] != user.name and name_count == 1:
            flash('昵称已经存在', 'err')
            return redirect(url_for('home.user'))

        phone_count = User.query.filter_by(phone=data['phone']).count()
        if data['phone'] != user.phone and phone_count == 1:
            flash('手机号码已经存在', 'err')
            return redirect(url_for('home.user'))

        email_count = User.query.filter_by(email=data['email']).count()
        if data['email'] != user.email and email_count == 1:
            flash('邮箱已经存在', 'err')
            return redirect(url_for('home.user'))

        user.name = data['name']
        user.email = data['email']
        user.phone = data['phone']
        user.info = data['info']
        db.session.add(user)
        db.session.commit()
        flash('修改成功', 'ok')
        return redirect(url_for('home.user'))
    return render_template("home/user.html", form=form, user=user)


@home.route("/pwd/", methods=["GET","POST"])
def pwd():
    user = User.query.all()
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
    return render_template("home/pwd.html",form=form,user=user)



@home.route("/detail/<int:id>/<int:page>/", methods=["GET","POST"])
def detail(id=None,page=None):
    image=Image.query.join(
        Tag
    ).filter(
        Tag.id == Image.tag_id,
        Image.id == int(id)
    ).first_or_404()
    page_data = Comment.query.join(
        Image
    ).join(
        User
    ).filter(
        Image.id == image.id,
        User.id == Comment.user_id
    ).order_by(
        Comment.addtime.desc()
    ).paginate(page=page, per_page=3)
    image.playnum = image.playnum + 1
    form = CommentForm()
    if "user" in session and form.validate_on_submit():
        data = form.data
        comment = Comment(
            content=data["content"],
            image_id=image.id,
            user_id=session["user_id"]
        )
        db.session.add(comment)
        db.session.commit()
        image.commentnum = image.commentnum+1
        db.session.add(image)
        db.session.commit()
        flash("提交评论成功",'ok')
        return redirect(url_for("home.detail",id=image.id,page=1))
    db.session.add(image)
    db.session.commit()
    return render_template("home/detail.html",image=image,form=form,page_data=page_data)


@home.route("/collect/add/",methods=["GET"])
def collect_add():
    uid = request.args.get("uid","")
    mid = request.args.get("mid","")
    collect = Collect.query.filter_by(
        user_id = int(uid),
        image_id = int(mid)
    ).count()
    if collect == 1:
        data = dict(ok=0)
    if collect == 0:
        collect = Collect(
            user_id=int(uid),
            movie_id=int(mid)
        )
        db.session.add(collect)
        db.session.commit()
        data = dict(ok=1)
    import json
    return json.dumps(data)