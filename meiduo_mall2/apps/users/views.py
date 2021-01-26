from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
import django
from django.views import View

from apps.users.models import User

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


