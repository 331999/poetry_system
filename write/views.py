from django.shortcuts import render, redirect
from django.views import View
from .form import PoetryForm
from .models import Poem

class SelfWrite(View):
    def get(self, request):
        # 在GET请求中，传递一个空表单和一个诗歌列表
        form = PoetryForm()
        poems = Poem.objects.all().order_by('-id')  # 查询所有诗歌数据
        return render(request, 'self_write_poetry.html', {'form': form, 'poems': poems})

    def post(self, request):
        form = PoetryForm(request.POST)
        if form.is_valid():
            poetry = form.save()
            return redirect('write:selfWrite')
        # 表单验证失败时，也要传递 poems 变量
        poems = Poem.objects.all().order_by('-id')
        return render(request, 'self_write_poetry.html', {'form': form, 'poems': poems})
