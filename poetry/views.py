from django.db.models import Q
from django.shortcuts import render
from django.views import View
from django.views.generic.list import ListView
from poetry.models import Poetry

class Dynasty(View):
    def get(self, request):
        return render(request, 'dynasty_detail.html')

# 响应自己写的诗
class WritePoetry(View):
    def get(self, request):
        return render(request, 'self_write_poetry.html')

class SelectRead(View):
    def get(self, request):
        return render(request, 'tangSong_masterpieces.html')

class libai(View):
    def get(self, request):
        poems = Poetry.objects.filter(poet_name='李白')  # 查询所有李白的诗
        return render(request, 'libai.html', context={'poems': poems})

class dufu(View):
    def get(self, request):
        poems = Poetry.objects.filter(poet_name='杜甫')  # 查询所有杜甫的诗
        return render(request, 'dufu.html', context={'poems': poems})

class dongpo(View):
    def get(self, request):
        poems = Poetry.objects.filter(poet_name='苏轼')  # 查询所有苏轼的诗
        return render(request, 'dongpo.html', context={'poems': poems})

class jiaxuan(View):
    def get(self, request):
        poems = Poetry.objects.filter(poet_name='辛弃疾')  # 查询所有辛弃疾的诗
        return render(request, 'jiaxuan.html', context={'poems': poems})

class chutang(View):
    def get(self, request):
        poems = Poetry.objects.filter(poet_dynasty='唐代')
        return render(request, 'chutang.html', context={'poems': poems})

class shengtang(View):
    def get(self, request):
        poems = Poetry.objects.filter(poet_dynasty='唐代')
        return render(request, 'shengtang.html', context={'poems': poems})

class wantang(View):
    def get(self, request):
        poems = Poetry.objects.filter(poet_dynasty='唐代')
        return render(request, 'wantang.html', context={'poems': poems})

class zhongtang(View):
    def get(self, request):
        poems = Poetry.objects.filter(poet_dynasty='唐代')
        return render(request, 'zhongtang.html', context={'poems': poems})

class wudai(View):
    def get(self, request):
        poems = Poetry.objects.filter(poet_dynasty='五代')  # 查询五代的诗
        return render(request, 'wudai.html', context={'poems': poems})

class beisong1(View):
    def get(self, request):
        poems = Poetry.objects.filter(poet_dynasty='宋代')  # 查询宋代的诗
        return render(request, 'beisong1.html', context={'poems': poems})

class beisong2(View):
    def get(self, request):
        return render(request, 'beisong2.html')

class nansong(View):
    def get(self, request):
        return render(request, 'nansong.html')
