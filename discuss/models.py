from django.db import models
from users.models import User
from django.conf import settings

class Topic(models.Model):
    """ 帖子 """
    topic_author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="用户")
    topic_title = models.CharField("标题", max_length=32)
    topic_content = models.TextField("内容", max_length=4096)
    topic_create_date = models.DateTimeField("创建日期", auto_now_add=True)
    topic_topped = models.BooleanField("置顶帖子", default=False)

    def __str__(self):
        # "#" + str(self.id) + " " + 李白的诗
        return "#" + str(self.id) + " " + self.topic_title
class Reply(models.Model):
    """ 回复 """
    reply_author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="作者")
    reply_content = models.TextField("内容", max_length=4096)
    reply_create_date = models.DateTimeField("创建时间", auto_now_add=True)
    reply_topic = models.ForeignKey("Topic", on_delete=models.CASCADE, verbose_name="所在帖子")

    def __str__(self):
        return "#" + str(
            self.id) + " " + self.reply_author.__str__() + " 在帖子 " + self.reply_topic.__str__() + " 的回复 " + self.reply_content
