from django.urls import path, re_path
from write import views

app_name = 'write'
urlpatterns = [
    # 响应挥毫泼墨页面
    path('selfWrite/', views.SelfWrite.as_view(), name='selfWrite'),

]
