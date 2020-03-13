from ..forms import BaseForms
from wtforms import StringField
from wtforms.validators import Regexp,EqualTo,ValidationError,InputRequired
from utils import zlcache

class Signup(BaseForms):
    telephone = StringField(validators=[Regexp(r"1[3|4|5|7|8][0-9]{9}",message="请输入正确格式的手机号")])
    cms_captcha = StringField()#Regexp(r"[0-9a-zA-Z]{6}",)
    username = StringField(validators=[Regexp(r".{2,20}", message="请输入正确格式的用户名")])
    password = StringField(validators=[Regexp(r"[0-9a-zA-Z_\.]{6,20}", message="请输入正确格式的密码")])
    password2 = StringField(validators=[EqualTo("password",message="密码不一致")])
    graph_captcha = StringField(validators=[Regexp(r"\w{4}", message="请输入正确格式的短信验证码")])


    def validate_sms_captcha(self,field):
        sms_captcha = field.data
        telephone = self.telephone.data

        sms_captcha_mem = zlcache.get(telephone)
        if not sms_captcha_mem or sms_captcha_mem.lower() != sms_captcha.lower:
            raise ValidationError(message="短信验证码错误")


    def validate_graph_captcha(self,field):
        graph_captcha = field.data
        graph_captcha_mem = zlcache.get(graph_captcha.lower())
        if not graph_captcha_mem:
            raise ValidationError(message="图形验证码错误")

class SigninForm(BaseForms):
    telephone = StringField(validators=[Regexp(r"1[3|4|5|7|8][0-9]{9}", message="请输入正确格式的手机号")])
    password = StringField(validators=[Regexp(r"[0-9a-zA-Z_\.]{6,20}", message="请输入正确格式的密码")])
    remember = StringField()