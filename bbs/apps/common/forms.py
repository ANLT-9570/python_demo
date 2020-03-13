from ..forms import BaseForms
from wtforms import StringField
from wtforms.validators import Regexp,InputRequired
import hashlib


class SMSCaptchaForm(BaseForms):
    telephone =StringField(validators=[Regexp(r'1[345789]\d{9}')])
    timestamp = StringField(validators=[Regexp(r'\d{13}')])
    sign = StringField(validators=[InputRequired(message="字段不能为空")])
    salt = 'fsdgsdfg56sfd/*dsfa'

    def validate(self):
        result = super(SMSCaptchaForm,self).validate()
        if not result:
            return False

        telephone = self.telephone.data
        timestamp = self.timestamp.data
        sign = self.sign.data

        sign2 = hashlib.md5((timestamp+telephone+self.salt).encode("utf-8")).hexdigest()
        print(sign)
        print(sign2)
        if sign == sign2:
            return  True
        else:
            return False