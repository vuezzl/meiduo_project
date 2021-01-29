import json
import re

from QQLoginTool.QQtool import OAuthQQ
from django.conf import settings
from django.contrib.auth import login
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views import View



from django_redis import get_redis_connection

from apps.oauth.models import OAuthQQUser
from apps.users.models import User
from meiduo_mall2.utils.secret import SecretOauth


class QQUserView(View):
    # qq登录成功回调
    def get(self,request):
        code = request.GET.get('code')
        if not code:
            return JsonResponse({'code': 400, 'errmsg': '缺少code参数'})
        oauth = OAuthQQ(client_id=settings.QQ_CLIENT_ID,
                        client_secret=settings.QQ_CLIENT_SECRET,
                        redirect_uri=settings.QQ_REDIRECT_URI,
                        )
        try:
            access_token = oauth.get_access_token(code)
            open_id = oauth.get_open_id(access_token)
        except Exception as e:


            return JsonResponse({'code': 400, 'errmsg': '获取qq信息失败'})

        try:
            oauth_qq = OAuthQQ.objects.get(open_id=open_id)
        except Exception as e:
            print('没绑定过')
            # oppenid要进行加密
            open_id = SecretOauth().dumps({'openid':open_id})
            return JsonResponse({'code': 300, 'errmsg': '还没有绑定','access_token':open_id})

        else:
            print('绑定过了')
            user = oauth_qq.user
            login(request,user)
            response = JsonResponse({'code': 0, 'errmsg': 'qq登录成功'})
            response.set_cookie('username',user.username,max_age=3600*24*14)


            return response
    # 绑定
    def post(self,request):
        # 接收参数
        data_dict = json.loads(request.body.decode())
        # 解析参数
        mobile = data_dict.get('mobile')
        password = data_dict.get('password')
        sms_code = data_dict.get('sms_code')
        access_token = data_dict.get('access_token')
        if not all([mobile,password,sms_code]):
            return JsonResponse({'code': 400, 'errmsg':'参数不齐'})
        if not re.match(r'^[a-zA-Z0-9]{8,20}$', password):
            return JsonResponse({'code': 400, 'errmsg': '密码格式不正确'})
        if not re.match(r'^1[3-9]\d{9}$', mobile):
            return JsonResponse({'code': 400, 'errmsg': '手机号格式不正确'})
            # 链接redis数据库
        redis_client = get_redis_connection('verify_code')
        redis_sms_code = redis_client.get(mobile)
        if not redis_sms_code:
            return JsonResponse({'code': 400, 'errmsg': '短信验证码过期了'})
        if not sms_code == redis_sms_code.decode():
            return JsonResponse({'code': 400, 'errmsg': '短信验证码有误'})
        # openid进行解密
        openid = SecretOauth().loads(access_token).get('openid')
        if not openid:
            return JsonResponse({'code':400,'errmsg':'openid失效了'})


        # 判断手机号是否存在
        try:
            user = User.objects.get(mobile=mobile)
        except:
            user = User.objects.create_user(username=mobile,password=password,mobile=mobile)
        else:
            if not user.check_password(password):
                return JsonResponse({'code': 400, 'errmsg': '用户名或密码错误'})
        try:
            OAuthQQUser.objects.create(openid=access_token,user=user)
        except:
            return JsonResponse({'code': 400, 'errmsg': '绑定失败了'})

        login(request,user)
        response = response = JsonResponse({'code': 0, 'errmsg': 'ok'})
        response.set_cookie('username',user.username,max_age=3600*24*14)


        return response





        pass




# 获取qq的登录网址
class QQURLView(View):
    def get(self,request):
        # 获取 QQ 登录页面网址
        # 创建 OAuthQQ 类的对象
        oauth = OAuthQQ(client_id=settings.QQ_CLIENT_ID,
                        client_secret=settings.QQ_CLIENT_SECRET,
                        redirect_uri=settings.QQ_REDIRECT_URI,
                        state=None)


        # 调用对象的获取qq地址方法
        login_url = oauth.get_qq_url()

        # 返回登录地址
        return JsonResponse({'code': 0, 'errmsg': 'OK', 'login_url': login_url})