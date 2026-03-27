from django.db import models


class Poetry(models.Model):
    poet_name = models.CharField(max_length=10, verbose_name='诗人名')
    poet_dynasty = models.CharField(max_length=5, verbose_name='朝代')
    poetry_name = models.CharField(max_length=50, verbose_name='古诗名')
    poetry_info = models.TextField(verbose_name='古诗内容')

    def __str__(self):
        return self.poetry_name

    class Meta:
        db_table = 'poetry_info'
        verbose_name = '古诗'


class Poet(models.Model):
    poet_name = models.CharField(max_length=100, verbose_name='诗人名')
    poet_info = models.TextField(verbose_name='诗人生平')
    poet_works = models.JSONField()

    def __str__(self):
        return self.poet_name

    class Meta:
        db_table = 'poet_info'
        verbose_name = '诗人'
