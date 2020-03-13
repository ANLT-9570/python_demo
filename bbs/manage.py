from flask_script import Manager
from flask_migrate import Migrate,MigrateCommand
from app import app
from exts import db
from apps.cms import models
from apps.front import models as front_models
from apps.models import BannerModel

CMSUser = models.CMSUser
CMSRole = models.CMSRole
CMSPermission = models.CMSPermission
front_user = front_models.FrontUser



manage = Manager(app)

Migrate(app,db)
manage.add_command('db',MigrateCommand)

@manage.option('-u','--username',dest = 'username')
@manage.option('-p','--password',dest = 'password')
@manage.option('-e','--email',dest = 'email')
def create_cns_user(username,password,email):
    user = CMSUser(username=username,password=password,email=email)
    db.session.add(user)
    db.session.commit()
    print("cms 添加通话成功！")

@manage.command
def create_role():
    #访问者
    visitor = CMSRole(name="访问者",desc="只能看相关的数据不能改")
    visitor.permissions = CMSPermission.VISTOR
    #运营
    operator = CMSRole(name="运营", desc="管理帖子，管理评论，管理前台用户")
    operator.permissions = CMSPermission.VISTOR | CMSPermission.POSTER  | CMSPermission.COMMENTER | CMSPermission.FRONTUSER
    #管理员
    admin = CMSRole(name="管理员", desc="拥有本系统的所有权限")
    admin.permissions = CMSPermission.VISTOR | CMSPermission.POSTER | CMSPermission.CMSUSER | CMSPermission.COMMENTER | CMSPermission.FRONTUSER | CMSPermission.BOARDER

    #开发者
    developer = CMSRole(name="开发者", desc="开发人员专用角色")
    developer.permissions = CMSPermission.ALL_PERMISSION

    db.session.add_all([visitor,operator,admin,developer])
    db.session.commit()

@manage.option('-e','--email',dest = 'email')
@manage.option('-n','--name',dest = 'name')
def add_user_to_role(email,name):
    user = CMSUser.query.filter_by(email = email).first()
    if user:
        role = CMSRole.query.filter_by(name=name).first()
        if role:
            role.users.append(user)
            db.session.commit()
            print("角色添加成功")
        else:
            print("没有这个角色 s%" % role)
    else:
        print("s% 邮箱没有这个用户 " % email)

@manage.command
def test_permissions():
    user = CMSUser.query.first()
    if user.has_permissions(CMSPermission.VISTOR):
        print("拥有这个角色")
    else:
        print("mei有这个角色")

@manage.option('-t','--telephone',dest = 'telephone')
@manage.option('-u','--username',dest = 'username')
@manage.option('-p','--password',dest = 'password')
def create_front_user(telephone,username,password):
    user = front_user(telephone = telephone,username = username,password = password)
    db.session.add(user)
    db.session.commit()


if __name__ == "__main__":
    manage.run()