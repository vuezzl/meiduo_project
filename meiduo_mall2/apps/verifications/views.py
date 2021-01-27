import random

from django import http
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views import View

from apps.verifications.libs.captcha.captcha import captcha
from redis import StrictRedis
from django_redis import get_redis_connection
# 短信验证码
from apps.verifications.libs.yuntongxun.ccp_sms import CCP


class SMSCodeView(View):
    def get(self,request,mobile):
        # 接收参数
        # 解析参数
        image_code = request.GET.get('image_code')
        uuid = request.GET.get('image_code_id')
        # 校验参数--判空
        if not all([image_code,uuid]):
            return JsonResponse({'code':400,'errmsg':'参数不齐'})
        # 将redis数据库存储的图形验证码取出来
        # 链接redis数据库
        redis_client = get_redis_connection('verify_code')
        redis_image_code = redis_client.get(uuid)
        # 如果取出的uuid是空的　　那么过期了
        if not redis_image_code:
            return JsonResponse({'code': 400, 'errmsg': '验证码过期了'})
        # 删除redis数据库中的验证码
        redis_client.delete(uuid)
        # 和前端比较验证码是否一致
        if not image_code  == redis_image_code.decode():
            return JsonResponse({'code': 400, 'errmsg': '验证码输入错误'})
        # 生成随机的６位验证码
        sms_code = random.randint(100000,999999)

        # 将手机号验证码存入redis数据库中
        redis_client.setex(mobile,300,sms_code)
        CCP().send_template_sms(mobile,[sms_code, 5],1)
        print('短信验证码:',sms_code)
        # @param to 手机号码
        # @param datas 内容数据 格式为数组 例如：{'12','34'}，如不需替换请填 ''
        # @param temp_id 模板Id

        return JsonResponse({'code':0,'errmsg':'短信发送成功'})





# 图片验证码
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


