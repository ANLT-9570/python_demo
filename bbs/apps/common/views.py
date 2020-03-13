from flask import Blueprint,request
from .forms import SMSCaptchaForm
from utils.aliyun.aliyunSmS import aliyunAPI
from utils import restful,zlcache
import json

bp = Blueprint("common",__name__,url_prefix="/common")

@bp.route("/")
def index():
    return "common index"

@bp.route("/sms_captchas",methods=["post"])
def sms_captcha():
    req = json.loads(request.get_data(as_text=True))
    #print(req["telephone"])
    #print(type(req))
    print(req)
    #form  = SMSCaptchaForm(req)
    #for key,value in data.items():
    telephone = req["telephone"]

    if telephone:
        #form.validate()
        #telephone = form.telephone.data
        code = aliyunAPI.get_code(1)
        zlcache.set(telephone, code)
        res = aliyunAPI.send_sms(telephone,code)
        print(code)
        return res
    else:
        return restful.paramError(message="参数错误")