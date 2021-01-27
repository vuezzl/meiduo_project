from django.contrib.auth import login
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
import django
from django.views import View
import json
from apps.users.models import User
import re
from django_redis import get_redis_connection

# 注册
from meiduo_mall2.settings.dev import logger


class RegisterView(View):
    def post(self,request):
        # 接收参数
        data_dict = json.loads(request.body.decode())
        # 解析参数
        username = data_dict.get('username')
        password = data_dict.get('password')
        password2 = data_dict.get('password2')
        mobile = data_dict.get('mobile')
        sms_code = data_dict.get('sms_code')
        allow = data_dict.get('allow')
        # 校验参数　--判空，判正则
        if not all(['username','password','password2','mobile','sms_code']):
            return JsonResponse({'code':400,'errmsg':'参数不完整'})
        if not re.match(r'^[a-zA-Z0-9_-]{5,20}$', username):
            return JsonResponse({'code':400,'errmsg':'用户名格式不正确'})
        if not re.match(r'^[a-zA-Z0-9]{8,20}$', password):
            return JsonResponse({'code': 400, 'errmsg': '密码格式不正确'})
        if not password == password2:
            return JsonResponse({'code': 400, 'errmsg': '两次密码输入不一致'})
        if not re.match(r'^1[3-9]\d{9}$', mobile):
            return JsonResponse({'code': 400, 'errmsg': '手机号格式不正确'})
        if allow == 'False':
            return JsonResponse({'code': 400, 'errmsg': '必须勾选同意'})

        # 链接redis数据库
        redis_client = get_redis_connection('verify_code')
        redis_sms_code = redis_client.get(mobile)
        if not redis_sms_code:
            return JsonResponse({'code': 400, 'errmsg': '短信验证码过期了'})
        if not sms_code == redis_sms_code.decode():
            return JsonResponse({'code': 400, 'errmsg': '短信验证码有误'})




        try:
            user = User.objects.create_user(username=username,password=password,mobile=mobile)
        except Exception as e:
            return JsonResponse({'code': 400, 'errmsg': '注册失败'})
        try:
            login(request,user)
        except Exception as e:
            return JsonResponse({'code': 400, 'errmsg': '保持登录失败'})

        return JsonResponse({'code':0,'errmsg':'ok'})


# 用户名重复
class UsernameCountView(View):
    def get(self,request,username):
        """接收参数，
        　　解析参数，
        　　校验参数．

        """
        count = User.objects.filter(username=username).count()
        data_dict = {
            'code':0,
            'errmsg': 'ok',
            'count':count

        }

        return JsonResponse(data_dict)


# 手机号重复

class MobileCountView(View):
    def get(self,request,mobile):
        count = User.objects.filter(mobile=mobile).count()
        data_dict = {
            'code': 0,
            'errmsg': 'ok',
            'count': count

        }

        return JsonResponse(data_dict)


