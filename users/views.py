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
        """显示密码重置页面或获取用户的安全问题"""
        username = request.GET.get('username')
        
        # 如果没有 username 参数，渲染页面
        if not username:
            return render(request, 'resetPassword.html')
        
        # 有 username 参数，返回安全问题（AJAX 请求）
        try:
            user = User.objects.get(username=username)
            if not user.security_question:
                return JsonResponse({'code': 400, 'msg': '该用户未设置安全问题'}, status=400)

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
                'email': request.user.email,
                'bio': request.user.bio,
            })

        errors = form.errors.get_json_data()
        first_error = list(errors.values())[0][0]['message'] if errors else '表单验证失败'
        return JsonResponse({'code': 400, 'msg': first_error}, status=400)


class StatsView(LoginRequiredMixin, View):
    """获取用户统计数据"""
    login_url = '/users/login/'

    def get(self, request):
        """获取统计数据"""
        user = request.user

        # 查询发表的诗歌数量
        poems_count = user.poet_info.count() if hasattr(user, 'poet_info') else 0

        # 查询发起的话题数量
        topics_count = 0
        if hasattr(user, 'discuss_topic'):
            topics_count = user.discuss_topic.filter(topic_author_id=user.id).count()

        # 查询参与的回复数量
        replies_count = 0
        if hasattr(user, 'discuss_topic'):
            # 获取用户发起的所有话题ID
            user_topic_ids = user.discuss_topic.filter(topic_author_id=user.id).values_list('id', flat=True)
            # 统计这些话题的回复数量
            if user_topic_ids.exists():
                replies_count = user.discuss_topic.filter(topic_author_id__in=user_topic_ids).count()

        return JsonResponse({
            'code': 200,
            'msg': 'OK',
            'poems_count': poems_count,
            'topics_count': topics_count,
            'replies_count': replies_count,
        })


class UpdateSecurityView(LoginRequiredMixin, View):
    """更新安全问题"""
    login_url = '/users/login/'

    def post(self, request):
        """更新安全问题"""
        security_question = request.POST.get('security_question')
        security_answer = request.POST.get('security_answer', '').lower().strip()

        if not security_question:
            return JsonResponse({'code': 400, 'msg': '请选择安全问题'}, status=400)

        if not security_answer:
            return JsonResponse({'code': 400, 'msg': '请输入当前答案'}, status=400)

        # 验证答案
        if request.user.security_answer.lower() != security_answer:
            return JsonResponse({'code': 400, 'msg': '答案错误，请重试'}, status=400)

        # 更新安全问题
        request.user.security_question = security_question
        request.user.save()

        return JsonResponse({
            'code': 200,
            'msg': '安全问题修改成功',
        })


class VerifySecurityView(LoginRequiredMixin, View):
    """验证安全问题"""
    login_url = '/users/login/'

    def post(self, request):
        """验证答案"""
        security_answer = request.POST.get('security_answer', '').lower().strip()

        if not security_answer:
            return JsonResponse({'code': 400, 'msg': '请输入答案'}, status=400)

        # 验证答案
        if request.user.security_answer.lower() != security_answer:
            return JsonResponse({'code': 400, 'msg': '答案错误，请重试'}, status=400)

        return JsonResponse({
            'code': 200,
            'msg': '答案验证成功',
        })
