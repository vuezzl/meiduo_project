from . import views
from django.urls import path



urlpatterns = [
    # 图片验证码
    path('image_codes/<uuid:uuid>/', views.ImageCodeView.as_view()),
    # 短信验证码
    path('sms_codes/<mobile:mobile>/', views.SMSCodeView.as_view()),

]
