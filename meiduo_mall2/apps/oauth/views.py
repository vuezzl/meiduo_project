from QQLoginTool.QQtool import OAuthQQ
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views import View


# qq登录成功回调
class QQUserView(View):
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

        return JsonResponse({'code': 0, 'errmsg': 'qq登录成功'})


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