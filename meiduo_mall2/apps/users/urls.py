from . import views
from django.urls import path



urlpatterns = [
    # 用户名重复
    path('usernames/<username:username>/count/', views.UsernameCountView.as_view()),
    # 手机号重复
    path('mobiles/<mobile:mobile>/count/', views.MobileCountView.as_view()),
    # 注册
    path('register/',views.RegisterView.as_view()),
    # 用户登录
    path('login/',views.LoginView.as_view()),
    # 退出登录
    path('logout/',views.LogoutView.as_view()),
    #用户中心--判断用户是否登录
    path('info/',views.UserInfoView.as_view()),
    # 添加和验证邮箱
    path('emails/', views.EmailView.as_view()),



]
