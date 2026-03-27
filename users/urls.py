from django.urls import path, re_path
from users import views

app_name = 'users'

urlpatterns = [
    # 用户登录逻辑
    path('login/', views.Login.as_view(), name='login'),

    # http://127.0.0.1:8000/users/username/202231101199/count
    # 判断用户名是否重复
    re_path('^username/(?P<username>\d{12})/count$', views.UsernameCountView.as_view()),
    # 用户注册路由
    path('register/', views.Register.as_view(), name='register'),

    # 展示个人中心
    path('personal/', views.Person.as_view(), name='personal'),

]
