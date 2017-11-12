from flask_wtf import FlaskForm
from wtforms.fields import SubmitField,StringField,PasswordField,TextAreaField,FileField
from wtforms.validators import DataRequired,Email,ValidationError,Regexp,EqualTo
from app.models import User

class RegisterForm(FlaskForm):
    name = StringField(
        label= "名称",
        validators=[
            DataRequired("请输入用户名")
        ],
        description="用户名",
        render_kw={
            "class":"form-control",
            "placeholder":"请输入用户名"
        }
    )
    email = StringField(
        label= "邮箱",
        validators=[
            DataRequired("请输入邮箱"),
            Email("邮箱格式不正确")
        ],
        description="邮箱",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入邮箱"
        }

    )
    phone = StringField(
        label="手机",
        validators=[
            DataRequired("请输入手机"),
            Regexp("1[3458]\\d{9}", message="手机格式不正确")
        ],
        description="手机",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入手机",
            # "required": "required"
        }
    )
    pwd = PasswordField(
        label="密码",
        validators=[
            DataRequired("请输入密码")
        ],
        description="密码",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入密码",
            # "required": "required"
        }
    )
    repwd = PasswordField(
        label="确认密码",
        validators=[
            DataRequired("请输入确认密码"),
            EqualTo('pwd', message='两次输入的密码不一致')
        ],
        description="确认密码",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入确认密码",
            # "required": "required"
        }
    )
    submit = SubmitField(
        '注册',
        render_kw={
            "class": "btn btn-success form-control",
        }
    )

    def validate_name(self, field):
        name = field.data
        user = User.query.filter_by(name=name).count()
        if user == 1:
            raise ValidationError("用户已经存在")

    def validate_email(self, field):
        email = field.data
        user = User.query.filter_by(email=email).count()
        if user == 1:
            raise ValidationError("邮箱已经存在")

    def validate_phone(self, field):
        phone = field.data
        user = User.query.filter_by(phone=phone).count()
        if user == 1:
            raise ValidationError("手机已经存在")

class LoginForm(FlaskForm):
    name = StringField(
        label="用户名",
        validators=[
            DataRequired("请输入用户名")
        ],
        description="账号",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入用户名",
        }
    )
    pwd = PasswordField(
        label="密码",
        validators=[
            DataRequired("请输入密码")
        ],
        description="密码",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入密码",
        }
    )
    submit = SubmitField(
        '登录',
        render_kw={
            "class": "btn btn-success form-control",
        }
    )
    def validate_name(self, field):
        name = field.data
        user = User.query.filter_by(name=name).count()
        if user != 1:
            raise ValidationError("用户不存在")


# 修改会员信息表单
class UserDetailForm(FlaskForm):
    name = StringField(
        label='昵称',
        validators=[
            DataRequired("请输入昵称"),

        ],
        description="昵称",
        render_kw={
            "class": "form-control ",
            "placeholder": "请输入昵称！",
        }
    )
    email = StringField(
        label="邮箱",
        validators=[
            DataRequired("请输入邮箱"),
            Email('邮箱格式不正确')

        ],
        description="邮箱",
        render_kw={
            "class": "form-control ",
            "placeholder": "请输入邮箱！",

        }
    )
    phone = StringField(
        label="手机号码",
        validators=[
            DataRequired("请输入手机号码"),
            Regexp('1[3578]\\d{9}', message='手机格式不正确')

        ],
        description="手机号码",
        render_kw={
            "class": "form-control ",
            "placeholder": "请输入手机号码！",

        }
    )
    face = FileField(
        label="头像",
        validators=[
            DataRequired("请上传头像")

        ],
        description="头像",
    )
    info = TextAreaField(
        label='简介',
        validators=[
            DataRequired("请输入简介")

        ],
        description="简介",
        render_kw={
            "class": "form-control",
            "rows": 10,

        }
    )
    submit = SubmitField(
        '保存修改',
        render_kw={"class": "btn btn-success form-control  ", }
    )

class PwdForm(FlaskForm):
    old_pwd = PasswordField(
        label="旧密码",
        validators=[
            DataRequired("请输入旧密码")
        ],
        description="旧密码",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入旧密码",
        }
    )
    new_pwd = PasswordField(
        label="新密码",
        validators=[
            DataRequired("请输入新密码")
        ],
        description="新密码",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入旧密码",
        }
    )
    submit = SubmitField(
        '修改密码',
        render_kw={
            "class": "btn btn-success form-control",
        }
    )

class CommentForm(FlaskForm):
    content = TextAreaField(
        label="内容" ,
        validators=[
            DataRequired("请输入内容和")
        ],
        description="内容",
        render_kw={
            "id": "input-content"
        }
    )
    submit = SubmitField(
        '评论',
        render_kw={
            "class": "btn btn-success",
            "id":"btn-sub"
        }
    )