from django import http
from django.shortcuts import render

# Create your views here.
from django.views import View

from apps.verifications.libs.captcha.captcha import captcha
from redis import StrictRedis
from django_redis import get_redis_connection
class ImageCodeView(View):
    def get(self,request,uuid):
        # 接收参数
        # 解析参数
        # 校验参数
        # text, image = captcha.generate_captcha()
        # client = StrictRedis(db=2)
        # client.setex(str(uuid),300,text)

        text, image = captcha.generate_captcha()
        # 链接redis数据库
        client = get_redis_connection('verify_code')
        client.setex(str(uuid),300,text)
        return http.HttpResponse(image,content_type = 'image/jpg')


