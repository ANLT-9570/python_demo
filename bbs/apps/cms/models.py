from exts import db
from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash

class CMSPermission(object):
    #使用255的二进制方式表示 1111 1111
    ALL_PERMISSION = 11111111
    #1访问者权限
    VISTOR =        0b00000001
    #2管理帖子权限
    POSTER =        0b00000010
    #3管理评论的权限
    COMMENTER =     0b00000100
    #4管理板块的权限
    BOARDER =       0b00001000
    #5管理前台用户的权限
    FRONTUSER =     0b00010000
    #6管理后台用户的权限
    CMSUSER =       0b00100000
    #7管理后台管理员的权限
    ADMINER =       0b01000000


cms_role_user = db.Table(
    'cms_role_user',
    db.Column('cms_role_id',db.Integer,db.ForeignKey('cms_role.id'),primary_key=True),
    db.Column('cms_user_id',db.Integer,db.ForeignKey('cms_user.id'),primary_key=True),
)

class CMSRole(db.Model):
    __tablename__ = "cms_role"
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    name = db.Column(db.String(50),nullable=False)
    desc = db.Column(db.String(100),nullable=False)
    create_time = db.Column(db.DateTime,default=datetime.now())
    permissions = db.Column(db.Integer,default=CMSPermission.VISTOR)

    users = db.relationship("CMSUser",secondary=cms_role_user,backref="roles")

class CMSUser(db.Model):
    __tablename__ = "cms_user"
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    username = db.Column(db.String(50),nullable=False)
    _password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    join_time = db.Column(db.Date,default=datetime.now())

    def __init__(self,username,password,email):
        self.username = username
        self.password = password
        self.email = email

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self,raw_password):
        print(raw_password)
        self._password = generate_password_hash(raw_password)

    def check_password(self,raw_password):
        dfg = self.password
        cas = raw_password
        result = check_password_hash(self.password, raw_password)
        return result

    @property
    def permissions(self):
        if not self.roles:
            return 0
        all_perssions = 0
        for role in self.roles:
            permissions = role.permissions
            all_perssions |= permissions
        return all_perssions

    def has_permissions(self,permissions):
        all_permissions = self.permissions
        result = all_permissions & permissions == permissions
        return result

    @property
    def has_developer(self):
        return self.has_perssionss(CMSPermission.ALL_PERMISSION)