from django.urls import path
from contents import views

urlpatterns = [
    # 响应首页
    path('', views.IndexView.as_view(), name='index'),
]
