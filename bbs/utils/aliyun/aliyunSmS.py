from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest
import config,random

class aliyunAPI(object):
    def send_sms(telephone,code):
        phone = telephone
        code = {"code":code}
        # client = AcsClient('<accessKeyId>', '<accessSecret>', 'default')
        client = AcsClient(config.ACCESS_KEY_ID, config.ACCESS_KEY_SECRET, 'default')
        request = CommonRequest()
        request.set_accept_format('json')
        request.set_domain('dysmsapi.aliyuncs.com')
        request.set_method('POST')
        request.set_protocol_type('https')  # https | http
        request.set_version('2017-05-25')
        # 以上部分是公用的不变
        request.set_action_name('SendSms')
        # set_action_name 这个是选择你调用的接口的名称，如：SendSms，SendBatchSms等
        request.add_query_param('RegionId', "default")
        # 这个参数也是固定的

        request.add_query_param('PhoneNumbers', phone)  # 发给谁
        request.add_query_param('SignName', "xc")  # 签名
        request.add_query_param('TemplateCode', "SMS_158546404")  # 模板编号
        request.add_query_param('TemplateParam', f"{code}")  # 发送验证码内容
        response = client.do_action_with_exception(request)
        print(str(response, encoding='utf-8'))
        return response

    def get_code(self):
        ret = ""
        for i in range(6):
            num = random.randint(0, 9)
            # num = chr(random.randint(48,57))#ASCII表示数字
            letter = chr(random.randint(97, 122))  # 取小写字母
            Letter = chr(random.randint(65, 90))  # 取大写字母
            s = str(random.choice([num, letter, Letter]))
            ret += s
        return ret


# if __name__ == '__main__':
    # template = {
    #     'code': '88888',
    # }
    #send_sms(template)