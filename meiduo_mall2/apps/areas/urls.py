from . import views
from django.urls import path



urlpatterns = [
    # 省
    path('areas/', views.ProvinceAreasView.as_view()),
    # 市区
    path('areas/<int:pk>/', views.SubAreasView.as_view()),

]
