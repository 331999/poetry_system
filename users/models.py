from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    # 定义用户认证模型类
    pass

    class Meta:
        db_table = 'user'
        verbose_name = '用户'
        verbose_name_plural = '用户'
