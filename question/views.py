from django.shortcuts import render, HttpResponse
from django.views import View
from django.http import JsonResponse, HttpResponseNotFound
from .bot.send_question import bot
import os

class Question(View):
    def get(self, request):
        return render(request, 'question.html')

    def post(self, request):
        # 获取前端传入的问题
        question = request.POST.get('question')
        print(question)

        if question is None:
            return JsonResponse({'answer': '你可以提问我有关古诗的问题'})
        if question == '你好':
            return JsonResponse(
                {'answer': '你好👋！我是人工智能助手，可以叫我夫子，很高兴见到你，欢迎问我有关古诗词的问题。'})
        answer = bot.chat_main(question)
        if not answer:
            return JsonResponse({'answer': '你可以提问我有关古诗词的问题'})
        # # 将答案发送回前端
        return JsonResponse({'code': 200, 'errmsg': 'OK', 'answer': answer})


class Img(View):
    def get(self, request, image_name):
        image_path = os.path.join('static/img', image_name)
        if os.path.exists(image_path):
            with open(image_path, 'rb') as f:
                img_data = f.read()
                return HttpResponse(img_data, content_type='image/jpg')
        else:
            return HttpResponseNotFound()
