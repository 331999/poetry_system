from django.shortcuts import render, redirect
from django.views import View
from django.http import JsonResponse
from .form import PoetryForm
from .models import Poem
import os
import random

class SelfWrite(View):
    def get(self, request):
        # 在GET请求中，传递一个空表单和一个诗歌列表
        form = PoetryForm()
        poems = Poem.objects.all().order_by('-id')  # 查询所有诗歌数据
        
        # 获取轮播图图片
        carousel_images = self.get_random_carousel_images()
        
        return render(request, 'self_write_poetry.html', {
            'form': form, 
            'poems': poems,
            'carousel_images': carousel_images
        })

    def post(self, request):
        form = PoetryForm(request.POST)
        if form.is_valid():
            poetry = form.save()
            # 检查是否是 AJAX 请求
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': True, 'message': '作品提交成功！'})
            return redirect('write:selfWrite')
        # 表单验证失败时，也要传递 poems 变量
        poems = Poem.objects.all().order_by('-id')
        # 检查是否是 AJAX 请求
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)
        return render(request, 'self_write_poetry.html', {'form': form, 'poems': poems})
    
    def get_random_carousel_images(self, num_images=8):
        """
        从指定文件夹中随机选择图片
        :param num_images: 需要的图片数量，默认3张
        :return: 图片路径列表
        """
        # 指定图片文件夹路径（相对于 static 文件夹）
        img_folder = 'carousel'  # 可以修改为其他文件夹，如 'blog/timeline'
        
        # 获取静态文件的绝对路径
        static_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static', 'img', img_folder)
        
        # 支持的图片格式
        valid_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.webp')
        
        # 获取文件夹中所有符合条件的图片
        try:
            all_images = [
                f for f in os.listdir(static_path) 
                if f.lower().endswith(valid_extensions)
            ]
        except FileNotFoundError:
            # 如果文件夹不存在，返回默认图片
            return ['img/1.png', 'img/2.png', 'img/3.png']
        
        # 如果图片数量不足，返回所有图片
        if len(all_images) <= num_images:
            selected_images = all_images
        else:
            # 随机选择指定数量的图片
            selected_images = random.sample(all_images, num_images)
        
        # 返回相对路径（用于模板中的 static 标签）
        return [f'img/{img_folder}/{img}' for img in selected_images]
