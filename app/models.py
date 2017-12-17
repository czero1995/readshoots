from datetime import datetime
from app import db

#会员
class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    pwd = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    phone = db.Column(db.String(11), unique=True)
    info = db.Column(db.Text)
    face = db.Column(db.String(255), unique=True)
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)
    comments = db.relationship('Comment', backref='user')
    collects = db.relationship('Collect', backref='user')

    def __repr__(self):
        return "<User %r>" % self.name
    def check_pwd(self,pwd):
        from werkzeug.security import check_password_hash
        return check_password_hash(self.pwd,pwd)

# 图片
class Image(db.Model):
    __tablename__ = "image"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), unique=True)
    info = db.Column(db.Text)
    img = db.Column(db.String(255), unique=True)
    playnum = db.Column(db.BigInteger)
    commentnum = db.Column(db.BigInteger)
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id'))
    comments = db.relationship('Comment', backref='image')
    collects = db.relationship('Collect', backref='image')

    def __repr__(self):
        return "<Image %r>" % self.title

    # 图片
class Banner(db.Model):
    __tablename__ = "banner"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), unique=True)
    info = db.Column(db.Text)
    img = db.Column(db.String(255), unique=True)
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id'))

    def __repr__(self):
        return "<Bane %r>" % self.title

# 标签
class Tag(db.Model):
    __tablename__ = "tag"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)
    image = db.relationship("Image", backref='tag')

    def __repr__(self):
        return "<Tag %r>" % self.name
# 评论
class Comment(db.Model):
    __tablename__ = "comment"
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    image_id = db.Column(db.Integer, db.ForeignKey('image.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)

    def __repr__(self):
        return "<Comment %r>" % self.id

# 图片收藏
class Collect(db.Model):
    __tablename__ = "collect"
    id = db.Column(db.Integer, primary_key=True)
    image_id = db.Column(db.Integer, db.ForeignKey('image.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)

    def __repr__(self):
        return "<Collect %r>" % self.id


#管理员
class Admin(db.Model):
    __tablename__ = "admin"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    pwd = db.Column(db.String(100))
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)
    def __repr__(self):
        return "<Admin %r>" % self.name
    def check_pwd(self,pwd):
        from werkzeug.security import check_password_hash
        return check_password_hash(self.pwd,pwd)

if __name__ == "__main__":
    db.create_all()
    # from werkzeug.security import generate_password_hash
    #
    # admin = Admin(
    #         name = "rick",
    #         pwd=generate_password_hash("abcd1234")
    # )
    # db.session.add(admin)
    # db.session.commit()