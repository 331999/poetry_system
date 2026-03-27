from django.urls import path, re_path
from discuss import views

urlpatterns = [
    path('discuss/', views.Discuss.as_view(), name='discuss'),

    path('create/', views.CreateTopic.as_view(), name="create"),  # 创建帖子 GET/POST

    path('topic/<int:topic_id>/', views.LookTopic.as_view(), name="topic"),  # 帖子 GET

    path('topic/<int:topic_id>/reply/', views.ReplyTopic.as_view(), name="reply"),  # 回复 POST

]
