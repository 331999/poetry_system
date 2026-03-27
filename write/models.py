from django.db import models


class Poem(models.Model):
    poet_name = models.CharField(max_length=50,verbose_name="作者名")
    poetry_name = models.CharField(max_length=20, verbose_name="古诗名")
    poetry_content = models.TextField(verbose_name="古诗内容")

    def __str__(self):
        return self.poetry_name
