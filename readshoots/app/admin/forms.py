
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField, TextAreaField, SelectField, SelectMultipleField
from wtforms.validators import DataRequired, ValidationError,EqualTo
from app.models import Admin,Tag

tags = Tag.query.all()
class LoginForm(FlaskForm):
    account = StringField(
        label="账号",
        validators=[
            DataRequired("请输入账号")
        ],
        description="账号",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入账号",
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
    submit = SubmitField(
        '登录',
        render_kw={
            "class": "btn btn-success form-control",
        }
    )

    def validate_account(self, filed):
        account = filed.data
        admin = Admin.query.filter_by(name=account).count()
        if admin == 0:
            raise ValidationError("账号不存在")

class TagForm(FlaskForm):
    name = StringField(
        label="名称",
        validators=[
            DataRequired("请输入标签!")
        ],
        description="标签",
        render_kw={
            "class": "from-contril",
            "id": "input_name",
            "placeholder": "请输入标签名称"
        }
    )
    submit = SubmitField(
        '编辑',
        render_kw={
            "class": "btn btn-primary",
        }
    )


class ImageForm(FlaskForm):
    title = StringField(
        label="标题",
        validators=[
            DataRequired("请输入标题!")
        ],
        description="片名",
        render_kw={
            "class": "from-control",
            "id": "input_title",
            "placeholder": "请输入标题"
        }
    )
    info = TextAreaField(
        label='简介',
        validators=[
            DataRequired("请输入简介")
        ],
        description="简介",
        render_kw={
            "class": "form-control",
            "row": "10"
        }
    )
    img = FileField(
        label="图片",
        validators=[
            DataRequired("请上传图片")
        ],
        description="图片",
    )

    tag_id = SelectField(
        label="标签",
        validators=[
            DataRequired("请选择标签")
        ],
        coerce=int,
        choices=[(v.id, v.name) for v in tags],
        description="标签",
        render_kw={
            "class": "form-control"
        }
    )

    submit = SubmitField(
        '编辑',
        render_kw={
            "class": "btn btn-primary",
        }
    )


class BannerForm(FlaskForm):
    title = StringField(
        label="标题",
        validators=[
            DataRequired("请输入标题!")
        ],
        description="片名",
        render_kw={
            "class": "from-control",
            "id": "input_title",
            "placeholder": "请输入标题"
        }
    )
    info = TextAreaField(
        label='简介',
        validators=[
            DataRequired("请输入简介")
        ],
        description="简介",
        render_kw={
            "class": "form-control",
            "row": "10"
        }
    )
    img = FileField(
        label="图片",
        validators=[
            DataRequired("请上传图片")
        ],
        description="图片",
    )

    submit = SubmitField(
        '编辑',
        render_kw={
            "class": "btn btn-primary",
        }
    )