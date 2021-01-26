from . import views
from django.urls import path



urlpatterns = [
    # 用户名重复
    path('usernames/<username:username>/count/', views.UsernameCountView.as_view()),
    # 手机号重复
    path('mobiles/<mobile:mobile>/count/', views.MobileCountView.as_view()),
]
