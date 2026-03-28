from django.contrib.auth import login, authenticate, logout
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

from users import forms
from users.models import User, SECURITY_QUESTIONS


class Register(View):
    """用户注册"""

    def get(self, request):
        context = {'security_questions': SECURITY_QUESTIONS}
        return render(request, 'loginRegister.html', context)

    def post(self, request):
        register_form = forms.RegisterForm(request.POST)
        if register_form.is_valid():
            username = register_form.cleaned_data['username']
            password = register_form.cleaned_data['password']
            security_question = register_form.cleaned_data['security_question']
            security_answer = register_form.cleaned_data['security_answer'].lower().strip()

            try:
                User.objects.create_user(
                    username=username,
                    password=password,
                    security_question=security_question,
                    security_answer=security_answer,
                )
                return JsonResponse({
                    'code': 200,
                    'msg': '注册成功',
                    'redirect_url': '/users/login/'
                })
            except Exception as e:
                return JsonResponse({'code': 500, 'msg': f'注册失败: {str(e)}'}, status=500)

        errors = register_form.errors.get_json_data()
        first_error = list(errors.values())[0][0]['message'] if errors else '表单验证失败'
        return JsonResponse({'code': 400, 'msg': first_error}, status=400)


class UsernameCountView(View):
    """检查用户名是否存在"""

    def get(self, request, username):
        count = User.objects.filter(username=username).count()
        return JsonResponse({'code': 200, 'msg': 'OK', 'count': count})


class Login(View):
    """用户登录"""

    def get(self, request):
        context = {'security_questions': SECURITY_QUESTIONS}
        return render(request, 'loginRegister.html', context)

    def post(self, request):
        login_form = forms.LoginForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            remembered = login_form.cleaned_data.get('remembered', False)

            user = authenticate(username=username, password=password)
            if user is None:
                return JsonResponse({'code': 401, 'msg': '学号或密码错误'}, status=401)

            # 设置 session 有效期
            if remembered:
                request.session.set_expiry(60 * 60 * 24 * 7)  # 7天
            else:
                request.session.set_expiry(0)  # 浏览器关闭失效

            login(request, user)

            # 获取 next 参数
            next_url = request.GET.get('next', '/')

            response = JsonResponse({
                'code': 200,
                'msg': '登录成功',
                'redirect_url': next_url
            })
            response.set_cookie('username', user.username, max_age=604800)

            return response

        errors = login_form.errors.get_json_data()
        first_error = list(errors.values())[0][0]['message'] if errors else '表单验证失败'
        return JsonResponse({'code': 400, 'msg': first_error}, status=400)


class Logout(View):
    """用户退出登录"""

    def post(self, request):
        logout(request)
        response = JsonResponse({'code': 200, 'msg': '退出成功', 'redirect_url': '/'})
        response.delete_cookie('username')
        return response

    def get(self, request):
        """支持 GET 方式退出"""
        logout(request)
        response = redirect('index')
        response.delete_cookie('username')
        return response


class ChangePassword(LoginRequiredMixin, View):
    """修改密码"""
    login_url = '/users/login/'

    def post(self, request):
        form = forms.ChangePasswordForm(request.POST)
        if not form.is_valid():
            errors = form.errors.get_json_data()
            first_error = list(errors.values())[0][0]['message'] if errors else '表单验证失败'
            return JsonResponse({'code': 400, 'msg': first_error}, status=400)

        old_password = form.cleaned_data['old_password']
        new_password = form.cleaned_data['new_password']

        if not request.user.check_password(old_password):
            return JsonResponse({'code': 400, 'msg': '旧密码错误'}, status=400)

        request.user.set_password(new_password)
        request.user.save()

        return JsonResponse({
            'code': 200,
            'msg': '密码修改成功，请重新登录',
            'redirect_url': '/users/login/'
        })


class ResetPassword(View):
    """密码重置"""

    def get(self, request):
        """获取用户的安全问题"""
        username = request.GET.get('username')
        if not username:
            return JsonResponse({'code': 400, 'msg': '请输入学号'}, status=400)

        try:
            user = User.objects.get(username=username)
            if not user.security_question:
                return JsonResponse({'code': 400, 'msg': '该用户未设置安全问题'}, status=400)

            # 返回安全问题文本
            question_text = dict(SECURITY_QUESTIONS).get(user.security_question, '')
            return JsonResponse({
                'code': 200,
                'msg': 'OK',
                'question': question_text,
                'question_key': user.security_question
            })
        except User.DoesNotExist:
            return JsonResponse({'code': 404, 'msg': '该学号不存在'}, status=404)

    def post(self, request):
        """重置密码"""
        form = forms.ResetPasswordForm(request.POST)
        if not form.is_valid():
            errors = form.errors.get_json_data()
            first_error = list(errors.values())[0][0]['message'] if errors else '表单验证失败'
            return JsonResponse({'code': 400, 'msg': first_error}, status=400)

        username = form.cleaned_data['username']
        security_answer = form.cleaned_data['security_answer'].lower().strip()
        new_password = form.cleaned_data['new_password']

        try:
            user = User.objects.get(username=username)

            if user.security_answer.lower() != security_answer:
                return JsonResponse({'code': 400, 'msg': '安全问题答案错误'}, status=400)

            user.set_password(new_password)
            user.save()

            return JsonResponse({
                'code': 200,
                'msg': '密码重置成功',
                'redirect_url': '/users/login/'
            })
        except User.DoesNotExist:
            return JsonResponse({'code': 404, 'msg': '用户不存在'}, status=404)


class Profile(LoginRequiredMixin, View):
    """个人中心"""
    login_url = '/users/login/'

    def get(self, request):
        """显示个人信息"""
        user = request.user
        context = {
            'user': user,
            'security_questions': SECURITY_QUESTIONS,
        }
        return render(request, 'personal.html', context)

    def post(self, request):
        """更新个人信息"""
        form = forms.ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return JsonResponse({
                'code': 200,
                'msg': '个人信息更新成功',
                'nickname': request.user.nickname,
                'bio': request.user.bio,
            })

        errors = form.errors.get_json_data()
        first_error = list(errors.values())[0][0]['message'] if errors else '表单验证失败'
        return JsonResponse({'code': 400, 'msg': first_error}, status=400)
