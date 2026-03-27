from django.shortcuts import render, HttpResponse
from django.views import View
from django.http import JsonResponse, HttpResponseNotFound
from .bot.send_question import bot
import os
# from openai import OpenAI

#
# class Question(View):
#     def get(self, request):
#         return render(request, 'question.html')
#
#     def post(self, request):
#         client = OpenAI(
#             api_key="sk-8CA9vewKMVCLDNQvKeY10ZcI1cOhsza35KWKyAn9jujPIXOL",
#             base_url="https://api.moonshot.cn/v1",
#         )
#
#         history = [
#             {"role": "system",
#              "content": "你是 Kimi，由 Moonshot AI 提供的人工智能助手，你更擅长中文和英文的对话。你会为用户提供安全，有帮助，准确的回答。同时，你会拒绝一切涉及恐怖主义，种族歧视，黄色暴力等问题的回答。Moonshot AI 为专有名词，不可翻译成其他语言。"}
#         ]
#
#         def chat(query, history):
#             history.append({
#                 "role": "user",
#                 "content": query
#             })
#             completion = client.chat.completions.create(
#                 model="moonshot-v1-8k",
#                 messages=history,
#                 temperature=0.3,
#             )
#             result = completion.choices[0].message.content
#             history.append({
#                 "role": "assistant",
#                 "content": result
#             })
#             return result
#
#             while True:
#                 query = request.POST.get('question')
#                 if query.lower() == "退出":
#                     break
#                 answer = chat(query, history)
#                 return JsonResponse({'code': 200, 'errmsg': 'OK', 'answer': answer})


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
