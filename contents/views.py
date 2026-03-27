from django.shortcuts import render
from django.views import View


# Create your views here.
class IndexView(View):
    """响应首页"""

    def get(self, request):
        return render(request, 'index.html')

