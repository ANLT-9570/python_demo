from wtforms import Form,StringField,IntegerField
from wtforms.validators import Email,InputRequired,Length,EqualTo
from ..forms import BaseForms
from utils import zlcache
from wtforms import ValidationError
from flask import g


class LoginForm(BaseForms):
    email = StringField(validators=[Email(message='请输入正确的邮箱格式'),InputRequired(message='请输入邮箱')])
    password = StringField(validators=[Length(6,20,message='请输入正确格式的密码')])
    remember = IntegerField()

class ResetPwdForm(BaseForms):
    oldpwd = StringField(validators=[Length(6,20,message='请输入正确格式的旧密码')])
    newpwd = StringField(validators=[Length(6, 20, message='请输入正确格式的新密码')])
    new2pwd = StringField(validators=[EqualTo("newpwd",message="确认密码不一致")])

class ResetMailForm(BaseForms):
    email = StringField(validators=[Email(message="请输入正确格式的邮箱")])
    captch = StringField(validators=[Length(min=6,max=6,message="请输入正确长度的验证码")])

    def validata_captch(self,field):
        captch = field.data
        email = self.email.data
        captch_cache = zlcache.get(email)
        if not captch_cache or captch.lower() != captch_cache.lower():
            raise ValidationError("邮箱验证码错误")

    def validate_email(self,field):
        email = field.data
        user = g.cms_user
        if user.email == email:
            raise ValidationError("不能修改为相同的邮箱")

class AddBannerForm(BaseForms):
    name = StringField(validators=[InputRequired(message="请输入轮播图名称")])
    image_url = StringField(validators=[InputRequired(message="请输入轮播图图片链接")])
    link_url = StringField(validators=[InputRequired(message="请输入轮播图跳转链接")])
    priority = IntegerField(validators=[InputRequired(message="请输入轮播图优先级")])
