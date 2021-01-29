from . import views
from django.urls import path



urlpatterns = [
    # qq的登录网址
    path('qq/authorization/', views.QQURLView.as_view()),
    # qq登录成功回调
    path('oauth_callback/', views.QQUserView.as_view()),

]
