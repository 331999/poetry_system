from django.urls import path, re_path
from users import views

app_name = 'users'

urlpatterns = [
    # 用户注册
    path('register/', views.Register.as_view(), name='register'),

    # 用户登录
    path('login/', views.Login.as_view(), name='login'),

    # 用户退出
    path('logout/', views.Logout.as_view(), name='logout'),

    # 检查用户名是否存在
    re_path(r'^username/(?P<username>\d{12})/count$', views.UsernameCountView.as_view(), name='check_username'),

    # 修改密码
    path('change-password/', views.ChangePassword.as_view(), name='change_password'),

    # 密码重置
    path('reset-password/', views.ResetPassword.as_view(), name='reset_password'),

    # 个人中心
    path('profile/', views.Profile.as_view(), name='profile'),
]
