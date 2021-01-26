from . import views
from django.urls import path



urlpatterns = [
    # 验证码
    path('image_codes/<uuid:uuid>/', views.ImageCodeView.as_view()),
]
