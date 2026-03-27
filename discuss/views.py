from django.http import Http404
from django.shortcuts import render, redirect
from django.views import View

from discuss.models import Topic, Reply
from users.models import User


class Discuss(View):
    def get(self, request):
        """ 首页 GET """
        # 将所有帖子按时间排序
        topics = Topic.objects.order_by('-topic_create_date')
        if request.user.is_authenticated:
            return render(request, 'discuss.html', {
                "topics": topics,
                "topped_topics": Topic.objects.filter(topic_topped=True).order_by('-topic_create_date'),
                "stats": {
                    "users": User.objects.count(),
                    "topics": Topic.objects.count(),
                    "replies": Reply.objects.count()
                },
            })
        else:
            return render(request, 'discuss.html', {
                "topics": topics,
                "stats": {
                    "users": User.objects.count(),
                    "topics": Topic.objects.count(),
                    "replies": Reply.objects.count()
                },
                "topped_topics": Topic.objects.filter(topic_topped=True).order_by('-topic_create_date')
            })


class CreateTopic(View):
    def get(self, request):
        """ 创建帖子 GET/POST """
        if request.user.is_authenticated:
            return render(request, 'create.html')
        else:
            return redirect('users:login')

    def post(self, request):
        if request.user.is_authenticated:
            form_title = request.POST.get('title')
            form_content = request.POST.get('content')

            if form_title == "" or form_content == "":
                return render(request, 'create.html', {
                    "error": "请填写完整信息",
                })

            topic = Topic(topic_title=form_title, topic_content=form_content, topic_author=request.user)
            topic.save()

        else:
            return redirect('users:login')
        return redirect('discuss')


class LookTopic(View):
    def get(self, request, topic_id):
        """ 帖子 GET """
        try:
            topic = Topic.objects.get(id=topic_id)
        except Exception:
            raise Http404("帖子不存在")

        # 验证用户是否登录
        if request.user.is_authenticated:
            return render(request, 'topic.html', {
                "topic": topic,
                "replies": Reply.objects.filter(reply_topic=topic),
                # "logged_in_user": request.session["logged_in_user"]
            })
        else:
            return render(request, 'loginRegister.html', {
                "topic": topic,
                "replies": Reply.objects.filter(reply_topic=topic)
            })


class ReplyTopic(View):
    def post(self, request, topic_id):
        """ 回复 POST """
        if request.user.is_authenticated:
            form_content = request.POST.get('content')
            form_author = User.objects.filter(username=request.user).first()
            form_topic = Topic.objects.filter(id=topic_id).first()

            if form_content != "":
                reply = Reply(reply_content=form_content, reply_topic=form_topic, reply_author=form_author)
                reply.save()
            return redirect(f'/topic/{topic_id}/')
        else:
            return redirect('/users/')
