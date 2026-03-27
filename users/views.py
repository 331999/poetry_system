from django.contrib.auth import login, authenticate
from django.http import JsonResponse, HttpResponseForbidden
from django.shortcuts import render, redirect
from django.views import View

from users import forms
from users.models import User

class Register(View):
    """实现用户注册逻辑"""

    def get(self, request):
        return render(request, 'loginRegister.html')

    def post(self, request):
        # 校验用户信息
        register_form = forms.RegisterForm(request.POST)
        print(register_form.is_valid())
        # 检查提交的表单数据是否符合在表单类中定义的验证规则
        if register_form.is_valid():
            # 数据合法，获取数据
            username = register_form.cleaned_data['username']
            password = register_form.cleaned_data['password']
            password2 = register_form.cleaned_data['password2']
            print(username, password)

            # 保存数据到数据库中
            try:
                user = User.objects.create_user(
                    username=username,
                    password=password,
                )
                print(user)
                # 保存用户到数据库
            except Exception as e:
                return render(request, 'loginRegister.html', {'register_error': '注册失败'})

            # 数据注册成功,可以进行登录
            return redirect('users:login')

        else:
            # 获取表单错误信息
            context = {'form_error': register_form.errors}
            return render(request, 'loginRegister.html', context=context)

class UsernameCountView(View):
    """判断用户名是否重复"""

    def get(self, request, username):
        # 从请求中获取用户名
        # 并从数据库中查看用户名是否存在
        count = User.objects.filter(username=username).count()
        return JsonResponse({'code': 200, 'errmsg': 'OK', 'count': count})

class Login(View):
    """用户登录逻辑"""

    def get(self, request):
        return render(request, 'loginRegister.html')

    def post(self, request):
        # 接受请求的参数进行校验
        login_form = forms.LoginForm(request.POST)
        # 判断数据是否正确
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']

            if not all([username, password]):
                return HttpResponseForbidden('缺少必要数据')

            # 认证用户数据
            # authenticate 用户存在则返回用户信息，不存在则返回None
            user = authenticate(username=username, password=password)
            if user is None:
                return render(request, 'loginRegister.html', {'account_errmsg': '账号或密码错误'})
            login(request, user)

            # 接收get请求中的next参数
            next = request.GET.get('next')
            print(f'next {next}')
            # 通过get请求判断有没有next参数
            if next:
                response = redirect(next)
            else:
                # 重定向到首页
                response = redirect('index')
            # 将用户数据接入cookie中
            response.set_cookie('username', user.username, 604800)

            return response
        else:
            context = {'form_error': login_form.errors}
            return render(request, 'loginRegister.html', context=context)

class Person(View):
    def get(self, request):
        return render(request, 'personal.html')
