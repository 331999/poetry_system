from django.db import models
from django.contrib.auth.models import AbstractUser


# 安全问题选项
SECURITY_QUESTIONS = [
    ('mother_name', '您母亲的姓名是？'),
    ('birth_city', '您的出生城市是？'),
    ('first_school', '您的第一所学校名称是？'),
    ('favorite_book', '您最喜欢的书籍是？'),
]


class User(AbstractUser):
    """用户模型"""
    nickname = models.CharField('昵称', max_length=50, blank=True, default='')
    avatar = models.ImageField('头像', upload_to='avatars/', blank=True, null=True)
    bio = models.TextField('个人简介', max_length=500, blank=True, default='')
    security_question = models.CharField(
        '安全问题',
        max_length=20,
        blank=True,
        choices=SECURITY_QUESTIONS
    )
    security_answer = models.CharField('安全问题答案', max_length=100, blank=True, default='')

    class Meta:
        db_table = 'user'
        verbose_name = '用户'
        verbose_name_plural = '用户'

    def __str__(self):
        return self.nickname or self.username

    def get_display_name(self):
        """获取显示名称：优先昵称，其次学号"""
        return self.nickname if self.nickname else self.username
