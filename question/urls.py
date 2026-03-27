from django.urls import path, re_path
from question import views


app_name = 'question'
urlpatterns = [

    # 问答界面
    path('find/', views.Question.as_view(), name='find'),


    # 加载图片
    # http://127.0.0.1:4673/question/img/xuezi.jpg
    re_path(r'^img/(?P<image_name>[A-Za-z]+\.jpg)$', views.Img.as_view()),


]
