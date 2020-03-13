from flask import jsonify

class HttpCode(object):
    ok = 200
    mqx = 40
    csc = 401
    ser = 500


def restful_result(code,message,data):
    return jsonify({"code":code,"message":message,"data":data})

def success(message="",data=None):
    return restful_result(code=HttpCode.ok,message=message,data=data)

def paramError(message="",data=None):
    return restful_result(code=HttpCode.csc,message=message,data=data)

def server_error():
    return restful_result(code=HttpCode.ser,message="服务器内部错误",data=None)