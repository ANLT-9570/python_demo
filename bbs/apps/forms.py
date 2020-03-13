
#from wtforms import Form
from flask_wtf import FlaskForm

class BaseForms(FlaskForm):

    def get_error(self):
        message = self.errors.popitem()[1][0]
        return message

    def validate(self):
        return super(BaseForms,self).validate()