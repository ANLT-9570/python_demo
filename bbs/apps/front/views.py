from flask import Blueprint,views,render_template,make_response,request,session
from utils import captcha
from io import BytesIO
from utils.aliyun.aliyunSmS import aliyunAPI
from utils import restful,zlcache
from .forms import Signup,SigninForm
from .models import FrontUser
from exts import db
import json,config

bp = Blueprint("front",__name__,url_prefix="/front")

@bp.route("/")
def index():
    return render_template("front/front_index.html")

@bp.route("/captchas")
def captchas():
    text,image = captcha.graph_captcha()
    zlcache.set(text.lower(),text.lower())
    out = BytesIO()
    image.save(out,'png')
    out.seek(0)
    resp = make_response(out.read())
    resp.content_type = 'image/png'
    return resp

@bp.route("/sms_captchas")
def sms_captchas():
    telephone = request.args.get("telephone")
    if not telephone:
        return restful.paramError(message="手机号不能为空")

    code = aliyunAPI.get_code(1)
    print("验证码:",code)
    res = aliyunAPI.send_sms(telephone=telephone,code=code)
    zlcache.set(telephone, code)
    return res

class Signin(views.MethodView):
    def get(self):
        return render_template("front/front_signin.html")
    def post(self):
        form = SigninForm(request.form)
        if form.validate():
            telephone = form.telephone.data
            password = form.password.data
            remember = form.remember.data

            user = FrontUser.query.filter_by(telephone = telephone).first()
            if user and user.check_password(password):
                session[config.FRONT_USER_ID] = user.id
                if remember:
                    session.permanent = True
                    return restful.success()
                else:
                    return restful.paramError(message="手机号或密码错误")
        else:
            return restful.paramError(message="手机号或密码错误")

class SignUpViews(views.MethodView):
    def get(self):
        return_to = request.referrer
        return render_template('front/front_signup.html',return_to=return_to)

    def post(self):
        rea = request.form
        form = Signup(request.form)
        if form.validate():
            telephone = form.telephone.data
            username = form.username.data
            password = form.password.data
            user = FrontUser(telephone=telephone,username=username,password=password)
            db.session.add(user)
            db.session.commit()
            return restful.success()

        else:
            print(form.get_error())
            return restful.paramError(message="出错了")

bp.add_url_rule('/signup',view_func=SignUpViews.as_view('signup'))
bp.add_url_rule('/front_signin',view_func=Signin.as_view('front_signin'))