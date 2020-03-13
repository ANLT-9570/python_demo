from flask import Blueprint,views,render_template,request,session,redirect,url_for,g,jsonify
from .forms import LoginForm,ResetPwdForm,ResetMailForm,AddBannerForm
from .models import CMSUser,CMSPermission
from .decorators import login_required,permissions_required
import config
from exts import db,mail
from flask_mail import Message
from utils import restful,zlcache
from ..models import BannerModel
import string,random
import json

bp = Blueprint("cms",__name__,url_prefix="/cms")

@bp.route("/")
@login_required
def index():
    return render_template("cms/index.html")

@bp.route('/logout')
@login_required
def logout():
    del session[config.CMS_USER_ID]
    return redirect(url_for('cms.login'))

@bp.route('/person')
@login_required
def person():
    return render_template('cms/cms_profile.html')

@bp.route("/p")
def test():
    user = CMSUser(username='123',password='2133',email='sd')
    user.password = '9999999'
    return user._password

@bp.route("/email")
def testEmail():
    message = Message('Test测试标题',recipients=['1516462994@qq.com'],body="测试的哈哈哈哈哈哈哈哈哈哈")
    mail.send(message)

@bp.route("/send_en_email/")
def SendEnEmail():
    email = request.args.get("email")
    if not email:
        return restful.paramError("请传递正确的邮箱参数")
    #随机生成字母
    ascm = string.ascii_letters
    source = list(ascm)
    #把数字合到source中
    source.extend(["0","1","2","3","4","5","6","7","8","9"])
    #随机取留个
    rd = random.sample(source,6)
    #拼接
    vrs = "".join(rd)
    #发送邮件
    message = Message("python学习测试邮箱",recipients=[email],body="您的验证码是：%s" % vrs)
    try:
        mail.send(message)
    except:
        return restful.server_error()
    zlcache.cache.set(email,vrs)
    return restful.success()

@bp.route("/posts")
@login_required
@permissions_required(CMSPermission.POSTER)
def posts():
    return render_template("cms/cms_posts.html")

@bp.route("/comments")
@login_required
@permissions_required(CMSPermission.COMMENTER)
def comments():
    return render_template("cms/cms_comments.html")

@bp.route("/boards")
@login_required
@permissions_required(CMSPermission.BOARDER)
def boards():
    return render_template("cms/cms_boards.html")

@bp.route("/fusers")
@login_required
@permissions_required(CMSPermission.FRONTUSER)
def fusers():
    return render_template("cms/cms_fusers.html")

@bp.route("/cusers")
@login_required
@permissions_required(CMSPermission.CMSUSER)
def cusers():
    return render_template("cms/cms_cusers.html")

@bp.route("/croles")
@login_required
@permissions_required(CMSPermission.ALL_PERMISSION)
def croles():
    return render_template("cms/cms_croles.html")

@bp.route("/banners")
@login_required
def banners():
    list = BannerModel.query.all()
    return render_template("cms/cms_banners.html",list=list)


@bp.route("/dbanners",methods=["get"])
@login_required
def dbanners():
    id = request.args.get("id")
    dd = request.form.get("id")
    if not id:
        return restful.paramError(message="cuowu")
    banner = BannerModel.query.get(id)
    if not banner:
        return restful.paramError(message="cuowu22")
    db.session.delete(banner)
    db.session.commit()
    return restful.success()


@bp.route("/ubanners",methods=["post"])
@login_required
def ubanners():
    req = json.loads(request.get_data(as_text=True))
    if req:
        id = req["id"];
        name = req["name"];
        image_url = req["image_url"];
        link_url = req["link_url"];
        priority = req["priority"];

        banner = BannerModel.query.get(id);
        if banner:
            banner.name=name
            banner.image_url = image_url
            banner.link_url = link_url
            banner.priority = priority
            db.session.commit()
            return restful.success()
        else:
            return restful.paramError(message="么有这个图")
    else:
        return restful.paramError(message="...")

@bp.route("/abanners",methods=["post"])
@login_required
def abanners():
    req = json.loads(request.get_data(as_text=True))

    #form = AddBannerForm(request.form)
    if req:
            #form.validate():
        name = req["name"];
        image_url = req["image_url"];
        link_url = req["link_url"];
        priority = req["priority"];

        banner = BannerModel(name=name,image_url=image_url,link_url=link_url,priority=priority)
        db.session.add(banner)
        db.session.commit()
        return restful.success()
    else:
        return restful.paramError(message="错误")

class LoginView(views.MethodView):

    def get(self,message=None):
        return render_template('cms/cms_login.html',message=message)
    def post(self):
        form = LoginForm(request.form)
        if form.validate():
            email = form.email.data
            password = form.password.data
            remember = form.remember.data

            user = CMSUser.query.filter_by(email=email).first()
            flask = user.check_password(password)
            if user and user.check_password(password):
                session[config.CMS_USER_ID] = user.id

                if remember:
                        #session.permanent = True
                        #则是31天
                    session.permanent = True
                return redirect(url_for('cms.index'))
            else:

                return self.get(message="邮箱或密码错误")
        else:
            print(form.errors)
            #{'password': ['请输入正确格式的密码']}
            #message = form.errors.popitem()
            #('password',['请输入正确格式的密码'])
            message = form.errors.popitem()[1][0]
            return self.get(message=message)

class ResetPwdView(views.MethodView):
    decorators = [login_required]
    def get(self):
        return render_template('cms/cms_resetpwd.html')
    def post(self):
        form = ResetPwdForm(request.form)
        if form.validate():
            oldpwd = form.oldpwd.data
            newpwd = form.newpwd.data
            user = g.cms_user
            if user.check_password(oldpwd):
                user.password = newpwd
                db.session.commit()
                return jsonify({"code":200,"message":""})
            else:
                return jsonify({"code": 400, "message": "旧密码错误"})
        else:
            message = form.get_error()
            return jsonify({"code": 400, "message": message})

class ResetMailView(views.MethodView):
    decorators = [login_required]
    def get(self):
        return render_template("cms/cms_resetmail.html")
    def post(self):
        form = ResetMailForm(request.form)
        e = form.email.data
        cp = form.captch.data
        form2 = ResetMailForm()
        e = form2.email.data
        cp = form2.captch.data

        f = form.validate()
        y = form2.validate()
        if form.validate():
            email = form.email.data
            g.cms_user.email = email
            db.session.commit()
            return restful.success()
        else:
            return restful.paramError(form.get_error())

bp.add_url_rule('/login',view_func=LoginView.as_view('login'))
bp.add_url_rule('/resetpwd/',view_func=ResetPwdView.as_view('resetpwd'))
bp.add_url_rule('/resetmail',view_func=ResetMailView.as_view('resetmail'))