# 用户认证系统完善 实现计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 完善古诗词鉴赏网的登录注册系统，添加退出登录、密码重置、用户信息扩展功能。

**Architecture:** 基于 Django 内置 auth 系统，扩展现有 User 模型添加新字段，采用表单验证 + AJAX 前端交互模式。

**Tech Stack:** Django 4.1, MySQL, JavaScript (axios), HTML/CSS

---

## 文件结构

### 后端文件
| 文件 | 职责 |
|------|------|
| `users/models.py` | User 模型定义，扩展字段 |
| `users/views.py` | 视图：注册、登录、退出、密码修改、密码重置、个人中心 |
| `users/urls.py` | URL 路由配置 |
| `users/forms.py` | 表单验证：注册、登录、密码修改、个人信息 |
| `users/admin.py` | Admin 后台配置 |
| `poetry_system/settings.py` | 项目配置：media、session |
| `poetry_system/urls.py` | 主路由：media 服务 |

### 前端文件
| 文件 | 职责 |
|------|------|
| `templates/loginRegister.html` | 登录注册页面（修改） |
| `templates/personal.html` | 个人中心页面（重写） |
| `templates/resetPassword.html` | 密码重置页面（新增） |
| `static/js/loginRegister.js` | 登录注册交互（修改） |
| `static/js/personal.js` | 个人中心交互（重写） |
| `static/js/resetPassword.js` | 密码重置交互（新增） |
| `static/css/personal.css` | 个人中心样式（新增） |
| `static/css/resetPassword.css` | 密码重置样式（新增） |

---

## Task 1: 扩展 User 模型

**Files:**
- Modify: `users/models.py`
- Modify: `users/admin.py`

- [ ] **Step 1: 修改 User 模型添加新字段**

```python
# users/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser


# 安全问题选项
SECURITY_QUESTIONS = [
    ('mother_name', '您母亲的姓名是？'),
    ('birth_city', '您的出生城市是？'),
    ('first_school', '您的第一所学校名称是？'),
    ('favorite_book', '您最喜欢的书籍是？'),
]


class User(AbstractUser):
    """用户模型"""
    nickname = models.CharField('昵称', max_length=50, blank=True, default='')
    avatar = models.ImageField('头像', upload_to='avatars/', blank=True, null=True)
    bio = models.TextField('个人简介', max_length=500, blank=True, default='')
    security_question = models.CharField(
        '安全问题',
        max_length=20,
        blank=True,
        choices=SECURITY_QUESTIONS
    )
    security_answer = models.CharField('安全问题答案', max_length=100, blank=True, default='')

    class Meta:
        db_table = 'user'
        verbose_name = '用户'
        verbose_name_plural = '用户'

    def __str__(self):
        return self.nickname or self.username

    def get_display_name(self):
        """获取显示名称：优先昵称，其次学号"""
        return self.nickname if self.nickname else self.username
```

- [ ] **Step 2: 更新 Admin 配置**

```python
# users/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from users.models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """用户管理"""
    list_display = ['username', 'nickname', 'email', 'is_active', 'is_staff']
    list_filter = ['is_active', 'is_staff']
    search_fields = ['username', 'nickname', 'email']

    fieldsets = BaseUserAdmin.fieldsets + (
        ('扩展信息', {
            'fields': ('nickname', 'avatar', 'bio', 'security_question', 'security_answer')
        }),
    )

    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('扩展信息', {
            'fields': ('nickname', 'avatar', 'bio', 'security_question', 'security_answer')
        }),
    )
```

- [ ] **Step 3: 创建数据库迁移**

```bash
cd D:/PycharmProjects/poetry_system
python manage.py makemigrations users
python manage.py migrate
```

- [ ] **Step 4: 提交**

```bash
git add users/models.py users/admin.py
git commit -m "feat(users): 扩展 User 模型添加昵称、头像、简介、安全问题字段"
```

---

## Task 2: 添加表单验证类

**Files:**
- Modify: `users/forms.py`

- [ ] **Step 1: 重写 forms.py 添加完整表单验证**

```python
# users/forms.py
from django import forms
from users.models import User, SECURITY_QUESTIONS


class RegisterForm(forms.Form):
    """注册表单"""
    username = forms.CharField(
        min_length=12,
        max_length=12,
        required=True,
        error_messages={
            'min_length': '学号必须为12位',
            'max_length': '学号必须为12位',
            'required': '学号不能为空',
        }
    )

    password = forms.CharField(
        min_length=8,
        max_length=20,
        required=True,
        error_messages={
            'min_length': '密码最小长度为8',
            'max_length': '密码最大长度为20',
            'required': '密码不能为空',
        }
    )

    password2 = forms.CharField(
        min_length=8,
        max_length=20,
        required=True,
        error_messages={
            'min_length': '密码最小长度为8',
            'max_length': '密码最大长度为20',
            'required': '确认密码不能为空',
        }
    )

    security_question = forms.ChoiceField(
        choices=SECURITY_QUESTIONS,
        required=True,
        error_messages={
            'required': '请选择安全问题',
        }
    )

    security_answer = forms.CharField(
        min_length=1,
        max_length=100,
        required=True,
        error_messages={
            'required': '请填写安全问题答案',
            'min_length': '答案不能为空',
        }
    )

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not username.isdigit():
            raise forms.ValidationError('学号必须为数字')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('该学号已被注册')
        return username

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if not any(c.isalpha() for c in password):
            raise forms.ValidationError('密码必须包含字母')
        if not any(c.isdigit() for c in password):
            raise forms.ValidationError('密码必须包含数字')
        return password

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')
        if password and password2 and password != password2:
            raise forms.ValidationError('两次输入的密码不一致')
        return cleaned_data


class LoginForm(forms.Form):
    """登录表单"""
    username = forms.CharField(
        min_length=12,
        max_length=12,
        required=True,
        error_messages={
            'min_length': '学号必须为12位',
            'max_length': '学号必须为12位',
            'required': '学号不能为空',
        }
    )

    password = forms.CharField(
        min_length=8,
        max_length=20,
        required=True,
        error_messages={
            'min_length': '密码长度不正确',
            'max_length': '密码长度不正确',
            'required': '密码不能为空',
        }
    )

    remembered = forms.BooleanField(required=False)


class ChangePasswordForm(forms.Form):
    """修改密码表单"""
    old_password = forms.CharField(required=True, error_messages={'required': '请输入旧密码'})
    new_password = forms.CharField(
        min_length=8,
        max_length=20,
        required=True,
        error_messages={
            'min_length': '新密码最小长度为8',
            'max_length': '新密码最大长度为20',
            'required': '请输入新密码',
        }
    )
    new_password2 = forms.CharField(
        min_length=8,
        max_length=20,
        required=True,
        error_messages={
            'min_length': '确认密码最小长度为8',
            'max_length': '确认密码最大长度为20',
            'required': '请确认新密码',
        }
    )

    def clean_new_password(self):
        password = self.cleaned_data.get('new_password')
        if not any(c.isalpha() for c in password):
            raise forms.ValidationError('新密码必须包含字母')
        if not any(c.isdigit() for c in password):
            raise forms.ValidationError('新密码必须包含数字')
        return password

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        new_password2 = cleaned_data.get('new_password2')
        if new_password and new_password2 and new_password != new_password2:
            raise forms.ValidationError('两次输入的新密码不一致')
        return cleaned_data


class ResetPasswordForm(forms.Form):
    """密码重置表单"""
    username = forms.CharField(
        min_length=12,
        max_length=12,
        required=True,
        error_messages={'required': '请输入学号'}
    )
    security_answer = forms.CharField(required=True, error_messages={'required': '请回答安全问题'})
    new_password = forms.CharField(
        min_length=8,
        max_length=20,
        required=True,
        error_messages={
            'min_length': '新密码最小长度为8',
            'max_length': '新密码最大长度为20',
            'required': '请输入新密码',
        }
    )
    new_password2 = forms.CharField(
        min_length=8,
        max_length=20,
        required=True,
        error_messages={'required': '请确认新密码'}
    )

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError('该学号不存在')
        return username

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        new_password2 = cleaned_data.get('new_password2')
        if new_password and new_password2 and new_password != new_password2:
            raise forms.ValidationError('两次输入的密码不一致')
        return cleaned_data


class ProfileForm(forms.ModelForm):
    """个人信息表单"""
    class Meta:
        model = User
        fields = ['nickname', 'avatar', 'bio']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 3, 'maxlength': 500}),
        }
        error_messages = {
            'nickname': {'max_length': '昵称最长50个字符'},
            'bio': {'max_length': '个人简介最长500个字符'},
        }
```

- [ ] **Step 2: 提交**

```bash
git add users/forms.py
git commit -m "feat(users): 添加注册、登录、修改密码、密码重置、个人信息表单验证"
```

---

## Task 3: 更新 URL 路由

**Files:**
- Modify: `users/urls.py`

- [ ] **Step 1: 更新用户模块路由**

```python
# users/urls.py
from django.urls import path, re_path
from users import views

app_name = 'users'

urlpatterns = [
    # 用户注册
    path('register/', views.Register.as_view(), name='register'),

    # 用户登录
    path('login/', views.Login.as_view(), name='login'),

    # 用户退出
    path('logout/', views.Logout.as_view(), name='logout'),

    # 检查用户名是否存在
    re_path(r'^username/(?P<username>\d{12})/count$', views.UsernameCountView.as_view(), name='check_username'),

    # 修改密码
    path('change-password/', views.ChangePassword.as_view(), name='change_password'),

    # 密码重置
    path('reset-password/', views.ResetPassword.as_view(), name='reset_password'),

    # 个人中心
    path('profile/', views.Profile.as_view(), name='profile'),
]
```

- [ ] **Step 2: 提交**

```bash
git add users/urls.py
git commit -m "feat(users): 添加退出登录、修改密码、密码重置、个人中心路由"
```

---

## Task 4: 重写视图函数

**Files:**
- Modify: `users/views.py`

- [ ] **Step 1: 重写完整视图**

```python
# users/views.py
import json
from django.contrib.auth import login, authenticate, logout
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
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
```

- [ ] **Step 2: 提交**

```bash
git add users/views.py
git commit -m "feat(users): 重写视图，添加退出登录、修改密码、密码重置、个人中心功能"
```

---

## Task 5: 更新项目配置

**Files:**
- Modify: `poetry_system/settings.py`
- Modify: `poetry_system/urls.py`

- [ ] **Step 1: 更新 settings.py 添加 media 和 session 配置**

在 `poetry_system/settings.py` 文件末尾添加：

```python
# Media files configuration
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Session configuration
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
SESSION_COOKIE_AGE = 60 * 60 * 24 * 7  # 7 days

# Login URL
LOGIN_URL = '/users/login/'
```

- [ ] **Step 2: 更新主 urls.py 添加 media 服务**

```python
# poetry_system/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('', include('contents.urls')),
    path('question/', include('question.urls')),
    path('dynasty/', include('poetry.urls')),
    path('', include('discuss.urls')),
    path('write/', include('write.urls')),
]

# 开发环境下提供 media 文件服务
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

- [ ] **Step 3: 创建 media 目录**

```bash
mkdir -p D:/PycharmProjects/poetry_system/media/avatars
```

- [ ] **Step 4: 提交**

```bash
git add poetry_system/settings.py poetry_system/urls.py
git commit -m "feat(config): 添加 media 配置和 session 配置"
```

---

## Task 6: 更新登录注册页面

**Files:**
- Modify: `templates/loginRegister.html`
- Modify: `static/js/loginRegister.js`

- [ ] **Step 1: 更新 loginRegister.html 添加安全问题和记住我**

```html
{% load static %}
<!DOCTYPE html>
<html lang="zh-CN">

<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width,initial-scale=1">
    <title>古诗词鉴赏网 - 登录注册</title>
    <link rel="stylesheet" href="{% static 'css/loginRegister.css' %}">
    <script src="{% static 'js/axios-0.18.0.min.js' %}"></script>
</head>

<body background="{% static 'img/loginRegister/background1.jpg' %}">
<button class="backToHomeBtn" id="backToHomeBtn">
    <a href="{% url 'index' %}"><img src="{% static 'img/loginRegister/backToHome.webp' %}" alt="返回首页"
                                     title="返回首页" class="BtnImg"></a>
</button>

<div class="container">
    <div class="form-box">
        <!-- 注册 -->
        <div class="register-box hidden">
            <form id="registerForm">
                {% csrf_token %}
                <h1>注册</h1>
                <input type="text" id="register_studentId" placeholder="学号（12位数字）">
                <span aria-live="polite" id="register_stuId"></span>

                <input type="password" placeholder="密码（8-20位，包含字母和数字）" id="pwd1">
                <span id="pwd1Span" aria-live="polite"></span>

                <input type="password" placeholder="确认密码" id="pwd2">
                <span id="pwd2Span" aria-live="polite"></span>

                <select id="securityQuestion" class="form-select">
                    <option value="">请选择安全问题</option>
                    {% for key, text in security_questions %}
                    <option value="{{ key }}">{{ text }}</option>
                    {% endfor %}
                </select>
                <span id="questionSpan" aria-live="polite"></span>

                <input type="text" id="securityAnswer" placeholder="安全问题答案">
                <span id="answerSpan" aria-live="polite"></span>

                <button type="submit" id="submitButton1" disabled>注册</button>
            </form>
        </div>
        <!-- 登录 -->
        <div class="login-box">
            <form id="loginForm">
                {% csrf_token %}
                <h1>登录</h1>
                <input type="text" id="login_studentId" placeholder="学号">
                <span aria-live="polite" id="login_stuId"></span>

                <input type="password" placeholder="密码" id="login_pwd">

                <div class="remember-me">
                    <input type="checkbox" id="remembered" name="remembered">
                    <label for="remembered">记住我（7天内免登录）</label>
                </div>

                <button type="submit" id="submitButton2">登录</button>

                <div class="forgot-password">
                    <a href="{% url 'users:reset_password' %}">忘记密码？</a>
                </div>
            </form>
        </div>
    </div>
    <div class="con-box left">
        <h2>欢迎来到<span>古诗词鉴赏网</span></h2>
        <p>快来结识你的<span>新朋友</span>吧</p>

        <img src="{% static 'img/loginRegister/register1.png' %}">
        <p>已有账号</p>
        <button id="login">去登录</button>
    </div>
    <div class="con-box right">
        <h2>欢迎来到<span>古诗词鉴赏网</span></h2>
        <p>快来结识你的<span>新朋友</span>吧</p>
        <img src="{% static 'img/loginRegister/login.png' %}">
        <p>没有账号？</p>
        <button id="register">去注册</button>
    </div>
</div>

<script src="{% static 'js/loginRegister.js' %}"></script>
<script type="module" src="https://unpkg.com/ionicons@7.1.0/dist/ionicons/ionicons.esm.js"></script>
<script nomodule src="https://unpkg.com/ionicons@7.1.0/dist/ionicons/ionicons.js"></script>

</body>
</html>
```

- [ ] **Step 2: 重写 loginRegister.js**

```javascript
// static/js/loginRegister.js

// 获取 CSRF token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');

// 配置 axios 默认携带 CSRF token
axios.defaults.headers.common['X-CSRFToken'] = csrftoken;

// 界面切换动画
let login = document.getElementById('login');
let login_box = document.getElementsByClassName('login-box')[0];
let register = document.getElementById('register');
let form_box = document.getElementsByClassName('form-box')[0];
let register_box = document.getElementsByClassName('register-box')[0];

login.addEventListener('click', () => {
    form_box.style.transform = 'translateX(0%)';
    register_box.classList.add('hidden');
    login_box.classList.remove('hidden');
});

register.addEventListener('click', () => {
    form_box.style.transform = 'translateX(80%)';
    login_box.classList.add('hidden');
    register_box.classList.remove('hidden');
});

// 注册表单验证
let allFieldsValid = false;

document.getElementById('register_studentId').addEventListener('input', function () {
    var studentId = this.value;
    var registerStuIdSpan = document.getElementById('register_stuId');

    if (studentId.length !== 12 || !/^\d+$/.test(studentId)) {
        registerStuIdSpan.textContent = '学号必须为12位数字';
        registerStuIdSpan.style.color = 'red';
        registerStuIdSpan.style.fontSize = '12px';
    } else {
        registerStuIdSpan.textContent = '';
    }
    checkAllFieldsValid();
});

document.getElementById('pwd1').addEventListener('input', function () {
    var pwd1 = this.value;
    var pwd1Span = document.getElementById('pwd1Span');

    if (pwd1.length < 8 || pwd1.length > 20) {
        pwd1Span.textContent = '密码长度必须在8到20位之间';
        pwd1Span.style.color = 'red';
        pwd1Span.style.fontSize = '12px';
    } else if (!/[a-zA-Z]/.test(pwd1) || !/\d/.test(pwd1)) {
        pwd1Span.textContent = '密码必须包含字母和数字';
        pwd1Span.style.color = 'red';
        pwd1Span.style.fontSize = '12px';
    } else {
        pwd1Span.textContent = '';
    }
    checkAllFieldsValid();
});

document.getElementById('pwd2').addEventListener('input', function () {
    var pwd1 = document.getElementById('pwd1').value;
    var pwd2 = this.value;
    var pwd2Span = document.getElementById('pwd2Span');

    if (pwd2 !== pwd1) {
        pwd2Span.textContent = '两次密码输入不匹配';
        pwd2Span.style.color = 'red';
        pwd2Span.style.fontSize = '12px';
    } else {
        pwd2Span.textContent = '';
    }
    checkAllFieldsValid();
});

document.getElementById('securityQuestion').addEventListener('change', function () {
    var questionSpan = document.getElementById('questionSpan');
    if (!this.value) {
        questionSpan.textContent = '请选择安全问题';
        questionSpan.style.color = 'red';
        questionSpan.style.fontSize = '12px';
    } else {
        questionSpan.textContent = '';
    }
    checkAllFieldsValid();
});

document.getElementById('securityAnswer').addEventListener('input', function () {
    var answerSpan = document.getElementById('answerSpan');
    if (!this.value.trim()) {
        answerSpan.textContent = '请填写安全问题答案';
        answerSpan.style.color = 'red';
        answerSpan.style.fontSize = '12px';
    } else {
        answerSpan.textContent = '';
    }
    checkAllFieldsValid();
});

function checkAllFieldsValid() {
    const studentId = document.getElementById('register_studentId').value;
    const pwd1 = document.getElementById('pwd1').value;
    const pwd2 = document.getElementById('pwd2').value;
    const question = document.getElementById('securityQuestion').value;
    const answer = document.getElementById('securityAnswer').value;

    allFieldsValid =
        studentId.length === 12 &&
        /^\d+$/.test(studentId) &&
        pwd1.length >= 8 &&
        pwd1.length <= 20 &&
        /[a-zA-Z]/.test(pwd1) &&
        /\d/.test(pwd1) &&
        pwd2 === pwd1 &&
        question !== '' &&
        answer.trim() !== '';

    document.getElementById('submitButton1').disabled = !allFieldsValid;
}

// 注册表单提交
document.getElementById('registerForm').addEventListener('submit', function (e) {
    e.preventDefault();

    var formData = new FormData();
    formData.append('username', document.getElementById('register_studentId').value);
    formData.append('password', document.getElementById('pwd1').value);
    formData.append('password2', document.getElementById('pwd2').value);
    formData.append('security_question', document.getElementById('securityQuestion').value);
    formData.append('security_answer', document.getElementById('securityAnswer').value);

    axios.post('/users/register/', formData)
        .then(response => {
            if (response.data.code === 200) {
                alert('注册成功！');
                window.location.href = response.data.redirect_url || '/users/login/';
            } else {
                alert(response.data.msg || '注册失败');
            }
        })
        .catch(error => {
            const msg = error.response?.data?.msg || '注册过程中发生错误，请稍后再试';
            alert(msg);
        });
});

// 登录表单验证
document.getElementById('login_studentId').addEventListener('input', function () {
    var studentId = this.value;
    var loginStuIdSpan = document.getElementById('login_stuId');

    if (studentId.length !== 12 || !/^\d+$/.test(studentId)) {
        loginStuIdSpan.textContent = '学号必须为12位数字';
        loginStuIdSpan.style.color = 'red';
        loginStuIdSpan.style.fontSize = '12px';
    } else {
        loginStuIdSpan.textContent = '';
    }
});

// 登录表单提交
document.getElementById('loginForm').addEventListener('submit', function (e) {
    e.preventDefault();

    var formData = new FormData();
    formData.append('username', document.getElementById('login_studentId').value);
    formData.append('password', document.getElementById('login_pwd').value);
    formData.append('remembered', document.getElementById('remembered').checked);

    axios.post('/users/login/', formData)
        .then(response => {
            if (response.data.code === 200) {
                alert('登录成功！');
                window.location.href = response.data.redirect_url || '/';
            } else {
                alert(response.data.msg || '登录失败');
            }
        })
        .catch(error => {
            const msg = error.response?.data?.msg || '登录过程中发生错误';
            alert(msg);
        });
});
```

- [ ] **Step 3: 添加样式到 loginRegister.css**

在 `static/css/loginRegister.css` 末尾添加：

```css
/* 安全问题选择器样式 */
.form-select {
    width: 100%;
    padding: 10px;
    margin: 10px 0;
    border: none;
    border-radius: 20px;
    background: rgba(255, 255, 255, 0.8);
    font-size: 14px;
}

.form-select:focus {
    outline: 2px solid #03e9f4;
}

/* 记住我样式 */
.remember-me {
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 10px 0;
    font-size: 14px;
    color: #fff;
}

.remember-me input[type="checkbox"] {
    margin-right: 8px;
    transform: scale(1.2);
}

.remember-me label {
    cursor: pointer;
}

/* 忘记密码链接 */
.forgot-password {
    text-align: center;
    margin-top: 15px;
}

.forgot-password a {
    color: #03e9f4;
    text-decoration: none;
    font-size: 14px;
}

.forgot-password a:hover {
    text-decoration: underline;
}
```

- [ ] **Step 4: 提交**

```bash
git add templates/loginRegister.html static/js/loginRegister.js static/css/loginRegister.css
git commit -m "feat(auth): 更新登录注册页面，添加安全问题和记住我功能"
```

---

## Task 7: 创建密码重置页面

**Files:**
- Create: `templates/resetPassword.html`
- Create: `static/js/resetPassword.js`
- Create: `static/css/resetPassword.css`

- [ ] **Step 1: 创建 resetPassword.html**

```html
{% load static %}
<!DOCTYPE html>
<html lang="zh-CN">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>密码重置 - 古诗词鉴赏网</title>
    <link rel="stylesheet" href="{% static 'css/resetPassword.css' %}">
    <script src="{% static 'js/axios-0.18.0.min.js' %}"></script>
</head>

<body background="{% static 'img/loginRegister/background1.jpg' %}">
<button class="back-to-home">
    <a href="{% url 'index' %}"><img src="{% static 'img/loginRegister/backToHome.webp' %}" alt="返回首页"
                                     title="返回首页"></a>
</button>

<div class="reset-container">
    <div class="reset-box">
        <h1>密码重置</h1>

        <!-- 步骤1: 输入学号 -->
        <div id="step1" class="step">
            <input type="text" id="username" placeholder="请输入学号">
            <span id="usernameSpan" aria-live="polite"></span>
            <button id="getQuestionBtn">获取安全问题</button>
        </div>

        <!-- 步骤2: 回答问题并设置新密码 -->
        <div id="step2" class="step hidden">
            <div class="question-display">
                <label>安全问题：</label>
                <p id="securityQuestion"></p>
            </div>

            <input type="text" id="securityAnswer" placeholder="请输入答案">
            <span id="answerSpan" aria-live="polite"></span>

            <input type="password" id="newPassword" placeholder="新密码（8-20位，含字母和数字）">
            <span id="pwdSpan" aria-live="polite"></span>

            <input type="password" id="confirmPassword" placeholder="确认新密码">
            <span id="confirmSpan" aria-live="polite"></span>

            <button id="resetBtn">重置密码</button>
        </div>

        <!-- 步骤3: 完成 -->
        <div id="step3" class="step hidden">
            <p class="success-msg">密码重置成功！</p>
            <a href="{% url 'users:login' %}" class="login-link">去登录</a>
        </div>

        <div class="back-link">
            <a href="{% url 'users:login' %}">返回登录</a>
        </div>
    </div>
</div>

<script src="{% static 'js/resetPassword.js' %}"></script>
</body>

</html>
```

- [ ] **Step 2: 创建 resetPassword.js**

```javascript
// static/js/resetPassword.js

// 获取 CSRF token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');
axios.defaults.headers.common['X-CSRFToken'] = csrftoken;

const step1 = document.getElementById('step1');
const step2 = document.getElementById('step2');
const step3 = document.getElementById('step3');
const getQuestionBtn = document.getElementById('getQuestionBtn');
const resetBtn = document.getElementById('resetBtn');

let currentUsername = '';

// 获取安全问题
getQuestionBtn.addEventListener('click', function () {
    const username = document.getElementById('username').value;
    const usernameSpan = document.getElementById('usernameSpan');

    if (!username || username.length !== 12 || !/^\d+$/.test(username)) {
        usernameSpan.textContent = '请输入正确的12位学号';
        usernameSpan.style.color = 'red';
        return;
    }

    usernameSpan.textContent = '';
    currentUsername = username;

    axios.get(`/users/reset-password/?username=${username}`)
        .then(response => {
            if (response.data.code === 200) {
                document.getElementById('securityQuestion').textContent = response.data.question;
                step1.classList.add('hidden');
                step2.classList.remove('hidden');
            } else {
                usernameSpan.textContent = response.data.msg || '获取安全问题失败';
                usernameSpan.style.color = 'red';
            }
        })
        .catch(error => {
            const msg = error.response?.data?.msg || '网络错误，请稍后再试';
            usernameSpan.textContent = msg;
            usernameSpan.style.color = 'red';
        });
});

// 验证密码
function validatePassword() {
    const pwd = document.getElementById('newPassword').value;
    const pwdSpan = document.getElementById('pwdSpan');

    if (pwd.length < 8 || pwd.length > 20) {
        pwdSpan.textContent = '密码长度必须在8到20位之间';
        pwdSpan.style.color = 'red';
        return false;
    }
    if (!/[a-zA-Z]/.test(pwd) || !/\d/.test(pwd)) {
        pwdSpan.textContent = '密码必须包含字母和数字';
        pwdSpan.style.color = 'red';
        return false;
    }

    pwdSpan.textContent = '';
    return true;
}

document.getElementById('newPassword').addEventListener('input', validatePassword);

document.getElementById('confirmPassword').addEventListener('input', function () {
    const pwd = document.getElementById('newPassword').value;
    const confirm = this.value;
    const confirmSpan = document.getElementById('confirmSpan');

    if (confirm !== pwd) {
        confirmSpan.textContent = '两次密码输入不一致';
        confirmSpan.style.color = 'red';
    } else {
        confirmSpan.textContent = '';
    }
});

// 重置密码
resetBtn.addEventListener('click', function () {
    const answer = document.getElementById('securityAnswer').value;
    const newPwd = document.getElementById('newPassword').value;
    const confirmPwd = document.getElementById('confirmPassword').value;

    const answerSpan = document.getElementById('answerSpan');

    if (!answer.trim()) {
        answerSpan.textContent = '请输入答案';
        answerSpan.style.color = 'red';
        return;
    }

    if (!validatePassword()) {
        return;
    }

    if (newPwd !== confirmPwd) {
        document.getElementById('confirmSpan').textContent = '两次密码输入不一致';
        document.getElementById('confirmSpan').style.color = 'red';
        return;
    }

    const formData = new FormData();
    formData.append('username', currentUsername);
    formData.append('security_answer', answer);
    formData.append('new_password', newPwd);
    formData.append('new_password2', confirmPwd);

    axios.post('/users/reset-password/', formData)
        .then(response => {
            if (response.data.code === 200) {
                step2.classList.add('hidden');
                step3.classList.remove('hidden');
            } else {
                alert(response.data.msg || '重置失败');
            }
        })
        .catch(error => {
            const msg = error.response?.data?.msg || '网络错误，请稍后再试';
            alert(msg);
        });
});
```

- [ ] **Step 3: 创建 resetPassword.css**

```css
/* static/css/resetPassword.css */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    min-height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
    background-size: cover;
    font-family: 'Microsoft YaHei', sans-serif;
}

.back-to-home {
    position: absolute;
    top: 20px;
    left: 20px;
    background: none;
    border: none;
    cursor: pointer;
}

.back-to-home img {
    width: 40px;
    height: 40px;
}

.reset-container {
    display: flex;
    justify-content: center;
    align-items: center;
}

.reset-box {
    background: rgba(255, 255, 255, 0.9);
    padding: 40px;
    border-radius: 20px;
    box-shadow: 0 15px 35px rgba(0, 0, 0, 0.3);
    width: 400px;
    text-align: center;
}

.reset-box h1 {
    margin-bottom: 30px;
    color: #333;
    font-size: 28px;
}

.step input {
    width: 100%;
    padding: 12px 20px;
    margin: 10px 0;
    border: 2px solid #ddd;
    border-radius: 25px;
    font-size: 14px;
    transition: border-color 0.3s;
}

.step input:focus {
    outline: none;
    border-color: #03e9f4;
}

.step input::placeholder {
    color: #aaa;
}

.step span {
    display: block;
    font-size: 12px;
    min-height: 18px;
    text-align: left;
    margin-left: 20px;
}

.step button {
    width: 100%;
    padding: 12px;
    margin-top: 20px;
    border: none;
    border-radius: 25px;
    background: linear-gradient(120deg, #03e9f4, #2196f3);
    color: #fff;
    font-size: 16px;
    cursor: pointer;
    transition: all 0.3s;
}

.step button:hover {
    background: linear-gradient(120deg, #2196f3, #03e9f4);
    box-shadow: 0 5px 15px rgba(3, 233, 244, 0.4);
}

.question-display {
    background: #f5f5f5;
    padding: 15px;
    border-radius: 10px;
    margin-bottom: 15px;
    text-align: left;
}

.question-display label {
    font-weight: bold;
    color: #666;
}

.question-display p {
    margin-top: 8px;
    color: #333;
    font-size: 16px;
}

.success-msg {
    color: #4caf50;
    font-size: 20px;
    margin-bottom: 20px;
}

.login-link {
    display: inline-block;
    padding: 12px 40px;
    background: linear-gradient(120deg, #03e9f4, #2196f3);
    color: #fff;
    text-decoration: none;
    border-radius: 25px;
    transition: all 0.3s;
}

.login-link:hover {
    box-shadow: 0 5px 15px rgba(3, 233, 244, 0.4);
}

.back-link {
    margin-top: 20px;
}

.back-link a {
    color: #666;
    text-decoration: none;
    font-size: 14px;
}

.back-link a:hover {
    color: #03e9f4;
}

.hidden {
    display: none !important;
}
```

- [ ] **Step 4: 提交**

```bash
git add templates/resetPassword.html static/js/resetPassword.js static/css/resetPassword.css
git commit -m "feat(auth): 添加密码重置页面"
```

---

## Task 8: 重写个人中心页面

**Files:**
- Modify: `templates/personal.html`
- Modify: `static/js/personal.js`
- Create: `static/css/personal.css`

- [ ] **Step 1: 重写 personal.html**

```html
{% load static %}
<!DOCTYPE html>
<html lang="zh-CN">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>个人中心 - 古诗词鉴赏网</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.14.0/css/all.min.css"/>
    <link rel="stylesheet" href="{% static 'css/personal.css' %}">
</head>

<body>
<div class="profile-container">
    <div class="profile-card">
        <div class="card-header">
            <div class="pic">
                {% if user.avatar %}
                <img src="{{ user.avatar.url }}" alt="头像">
                {% else %}
                <img src="{% static 'img/default-avatar.png' %}" alt="默认头像">
                {% endif %}
            </div>
            <div class="name">{{ user.nickname|default:user.username }}</div>
            <div class="username">学号: {{ user.username }}</div>

            <div class="actions">
                <button class="action-btn" id="editProfileBtn">
                    <i class="fas fa-edit"></i> 编辑资料
                </button>
                <button class="action-btn" id="changePasswordBtn">
                    <i class="fas fa-key"></i> 修改密码
                </button>
                <button class="action-btn logout" id="logoutBtn">
                    <i class="fas fa-sign-out-alt"></i> 退出登录
                </button>
            </div>
        </div>

        <div class="card-body">
            <div class="info-item">
                <span class="label"><i class="fas fa-user"></i> 昵称</span>
                <span class="value">{{ user.nickname|default:"未设置" }}</span>
            </div>
            <div class="info-item">
                <span class="label"><i class="fas fa-info-circle"></i> 个人简介</span>
                <span class="value">{{ user.bio|default:"这个人很懒，什么都没写~" }}</span>
            </div>
        </div>
    </div>
</div>

<!-- 编辑资料模态框 -->
<div class="modal" id="editModal">
    <div class="modal-content">
        <div class="modal-header">
            <h2>编辑个人资料</h2>
            <button class="close-btn" id="closeEditModal">&times;</button>
        </div>
        <form id="profileForm">
            {% csrf_token %}
            <div class="form-group">
                <label for="nickname">昵称</label>
                <input type="text" id="nickname" name="nickname" value="{{ user.nickname }}"
                       maxlength="50" placeholder="请输入昵称">
            </div>
            <div class="form-group">
                <label for="avatar">头像</label>
                <input type="file" id="avatar" name="avatar" accept="image/*">
                <div class="avatar-preview" id="avatarPreview"></div>
            </div>
            <div class="form-group">
                <label for="bio">个人简介</label>
                <textarea id="bio" name="bio" maxlength="500" rows="4"
                          placeholder="介绍一下自己吧~">{{ user.bio }}</textarea>
            </div>
            <div class="form-actions">
                <button type="button" class="cancel-btn" id="cancelEditBtn">取消</button>
                <button type="submit" class="save-btn">保存</button>
            </div>
        </form>
    </div>
</div>

<!-- 修改密码模态框 -->
<div class="modal" id="passwordModal">
    <div class="modal-content">
        <div class="modal-header">
            <h2>修改密码</h2>
            <button class="close-btn" id="closePasswordModal">&times;</button>
        </div>
        <form id="passwordForm">
            {% csrf_token %}
            <div class="form-group">
                <label for="oldPassword">旧密码</label>
                <input type="password" id="oldPassword" name="old_password" required
                       placeholder="请输入旧密码">
                <span id="oldPwdSpan" class="error-msg"></span>
            </div>
            <div class="form-group">
                <label for="newPassword">新密码</label>
                <input type="password" id="newPassword" name="new_password" required
                       placeholder="8-20位，包含字母和数字">
                <span id="newPwdSpan" class="error-msg"></span>
            </div>
            <div class="form-group">
                <label for="confirmPassword">确认新密码</label>
                <input type="password" id="confirmPassword" name="new_password2" required
                       placeholder="再次输入新密码">
                <span id="confirmSpan" class="error-msg"></span>
            </div>
            <div class="form-actions">
                <button type="button" class="cancel-btn" id="cancelPasswordBtn">取消</button>
                <button type="submit" class="save-btn">确认修改</button>
            </div>
        </form>
    </div>
</div>

<!-- 返回首页按钮 -->
<a href="{% url 'index' %}" class="back-home-btn">
    <i class="fas fa-home"></i> 返回首页
</a>

<script src="{% static 'js/personal.js' %}"></script>
</body>

</html>
```

- [ ] **Step 2: 重写 personal.js**

```javascript
// static/js/personal.js

// 获取 CSRF token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');
axios.defaults.headers.common['X-CSRFToken'] = csrftoken;

// 模态框操作
const editModal = document.getElementById('editModal');
const passwordModal = document.getElementById('passwordModal');
const editProfileBtn = document.getElementById('editProfileBtn');
const changePasswordBtn = document.getElementById('changePasswordBtn');
const logoutBtn = document.getElementById('logoutBtn');

// 打开编辑资料模态框
editProfileBtn.addEventListener('click', () => {
    editModal.style.display = 'flex';
});

// 打开修改密码模态框
changePasswordBtn.addEventListener('click', () => {
    passwordModal.style.display = 'flex';
});

// 关闭模态框
document.getElementById('closeEditModal').addEventListener('click', () => {
    editModal.style.display = 'none';
});

document.getElementById('closePasswordModal').addEventListener('click', () => {
    passwordModal.style.display = 'none';
    clearPasswordForm();
});

document.getElementById('cancelEditBtn').addEventListener('click', () => {
    editModal.style.display = 'none';
});

document.getElementById('cancelPasswordBtn').addEventListener('click', () => {
    passwordModal.style.display = 'none';
    clearPasswordForm();
});

// 点击模态框外部关闭
window.addEventListener('click', (e) => {
    if (e.target === editModal) {
        editModal.style.display = 'none';
    }
    if (e.target === passwordModal) {
        passwordModal.style.display = 'none';
        clearPasswordForm();
    }
});

// 头像预览
document.getElementById('avatar').addEventListener('change', function (e) {
    const file = e.target.files[0];
    const preview = document.getElementById('avatarPreview');

    if (file) {
        const reader = new FileReader();
        reader.onload = function (e) {
            preview.innerHTML = `<img src="${e.target.result}" alt="预览">`;
        };
        reader.readAsDataURL(file);
    } else {
        preview.innerHTML = '';
    }
});

// 编辑资料表单提交
document.getElementById('profileForm').addEventListener('submit', function (e) {
    e.preventDefault();

    const formData = new FormData(this);

    axios.post('/users/profile/', formData)
        .then(response => {
            if (response.data.code === 200) {
                alert('资料更新成功！');
                window.location.reload();
            } else {
                alert(response.data.msg || '更新失败');
            }
        })
        .catch(error => {
            const msg = error.response?.data?.msg || '网络错误';
            alert(msg);
        });
});

// 密码验证
function validateNewPassword() {
    const pwd = document.getElementById('newPassword').value;
    const span = document.getElementById('newPwdSpan');

    if (pwd.length < 8 || pwd.length > 20) {
        span.textContent = '密码长度必须在8到20位之间';
        return false;
    }
    if (!/[a-zA-Z]/.test(pwd) || !/\d/.test(pwd)) {
        span.textContent = '密码必须包含字母和数字';
        return false;
    }

    span.textContent = '';
    return true;
}

document.getElementById('newPassword').addEventListener('input', validateNewPassword);

document.getElementById('confirmPassword').addEventListener('input', function () {
    const pwd = document.getElementById('newPassword').value;
    const confirm = this.value;
    const span = document.getElementById('confirmSpan');

    span.textContent = confirm !== pwd ? '两次密码输入不一致' : '';
});

// 修改密码表单提交
document.getElementById('passwordForm').addEventListener('submit', function (e) {
    e.preventDefault();

    if (!validateNewPassword()) {
        return;
    }

    const newPwd = document.getElementById('newPassword').value;
    const confirmPwd = document.getElementById('confirmPassword').value;

    if (newPwd !== confirmPwd) {
        document.getElementById('confirmSpan').textContent = '两次密码输入不一致';
        return;
    }

    const formData = new FormData(this);

    axios.post('/users/change-password/', formData)
        .then(response => {
            if (response.data.code === 200) {
                alert(response.data.msg || '密码修改成功，请重新登录');
                window.location.href = response.data.redirect_url || '/users/login/';
            } else {
                alert(response.data.msg || '修改失败');
            }
        })
        .catch(error => {
            const msg = error.response?.data?.msg || '网络错误';
            alert(msg);
        });
});

// 清空密码表单
function clearPasswordForm() {
    document.getElementById('passwordForm').reset();
    document.getElementById('oldPwdSpan').textContent = '';
    document.getElementById('newPwdSpan').textContent = '';
    document.getElementById('confirmSpan').textContent = '';
}

// 退出登录
logoutBtn.addEventListener('click', function () {
    if (confirm('确定要退出登录吗？')) {
        axios.post('/users/logout/')
            .then(response => {
                window.location.href = response.data.redirect_url || '/';
            })
            .catch(error => {
                // 如果 POST 失败，尝试 GET
                window.location.href = '/users/logout/';
            });
    }
});
```

- [ ] **Step 3: 创建 personal.css**

```css
/* static/css/personal.css */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    min-height: 100vh;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    font-family: 'Microsoft YaHei', sans-serif;
    padding: 20px;
}

.profile-container {
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: calc(100vh - 40px);
}

.profile-card {
    background: #fff;
    border-radius: 20px;
    box-shadow: 0 15px 35px rgba(0, 0, 0, 0.2);
    overflow: hidden;
    width: 400px;
    max-width: 100%;
}

.card-header {
    background: linear-gradient(135deg, #03e9f4 0%, #2196f3 100%);
    padding: 30px;
    text-align: center;
    color: #fff;
}

.pic {
    width: 100px;
    height: 100px;
    border-radius: 50%;
    overflow: hidden;
    border: 4px solid #fff;
    margin: 0 auto 15px;
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
}

.pic img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.name {
    font-size: 24px;
    font-weight: bold;
    margin-bottom: 5px;
}

.username {
    font-size: 14px;
    opacity: 0.8;
}

.actions {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 10px;
    margin-top: 20px;
}

.action-btn {
    padding: 8px 16px;
    border: none;
    border-radius: 20px;
    background: rgba(255, 255, 255, 0.2);
    color: #fff;
    font-size: 14px;
    cursor: pointer;
    transition: all 0.3s;
}

.action-btn:hover {
    background: rgba(255, 255, 255, 0.3);
}

.action-btn.logout {
    background: rgba(244, 67, 54, 0.6);
}

.action-btn.logout:hover {
    background: rgba(244, 67, 54, 0.8);
}

.card-body {
    padding: 20px 30px;
}

.info-item {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    padding: 15px 0;
    border-bottom: 1px solid #eee;
}

.info-item:last-child {
    border-bottom: none;
}

.info-item .label {
    color: #666;
    font-size: 14px;
}

.info-item .label i {
    margin-right: 8px;
    width: 16px;
}

.info-item .value {
    color: #333;
    font-size: 14px;
    text-align: right;
    max-width: 200px;
    word-break: break-all;
}

/* 模态框样式 */
.modal {
    display: none;
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.5);
    justify-content: center;
    align-items: center;
    z-index: 1000;
}

.modal-content {
    background: #fff;
    border-radius: 15px;
    width: 400px;
    max-width: 90%;
    max-height: 90vh;
    overflow-y: auto;
}

.modal-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 20px;
    border-bottom: 1px solid #eee;
}

.modal-header h2 {
    font-size: 18px;
    color: #333;
}

.close-btn {
    background: none;
    border: none;
    font-size: 24px;
    cursor: pointer;
    color: #999;
}

.close-btn:hover {
    color: #333;
}

.form-group {
    padding: 0 20px;
    margin-bottom: 15px;
}

.form-group:first-of-type {
    margin-top: 20px;
}

.form-group label {
    display: block;
    margin-bottom: 8px;
    color: #333;
    font-size: 14px;
    font-weight: 500;
}

.form-group input,
.form-group textarea {
    width: 100%;
    padding: 10px 15px;
    border: 1px solid #ddd;
    border-radius: 8px;
    font-size: 14px;
    transition: border-color 0.3s;
}

.form-group input:focus,
.form-group textarea:focus {
    outline: none;
    border-color: #03e9f4;
}

.form-group textarea {
    resize: vertical;
}

.form-group .error-msg {
    display: block;
    color: #f44336;
    font-size: 12px;
    margin-top: 5px;
    min-height: 16px;
}

.avatar-preview {
    margin-top: 10px;
}

.avatar-preview img {
    width: 80px;
    height: 80px;
    border-radius: 50%;
    object-fit: cover;
}

.form-actions {
    display: flex;
    justify-content: flex-end;
    gap: 10px;
    padding: 20px;
    border-top: 1px solid #eee;
}

.cancel-btn,
.save-btn {
    padding: 10px 25px;
    border: none;
    border-radius: 8px;
    font-size: 14px;
    cursor: pointer;
    transition: all 0.3s;
}

.cancel-btn {
    background: #f5f5f5;
    color: #666;
}

.cancel-btn:hover {
    background: #e0e0e0;
}

.save-btn {
    background: linear-gradient(135deg, #03e9f4 0%, #2196f3 100%);
    color: #fff;
}

.save-btn:hover {
    box-shadow: 0 5px 15px rgba(3, 233, 244, 0.3);
}

.back-home-btn {
    position: fixed;
    top: 20px;
    left: 20px;
    padding: 10px 20px;
    background: rgba(255, 255, 255, 0.9);
    color: #333;
    text-decoration: none;
    border-radius: 25px;
    font-size: 14px;
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
    transition: all 0.3s;
}

.back-home-btn:hover {
    background: #fff;
    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.15);
}

.back-home-btn i {
    margin-right: 8px;
}
```

- [ ] **Step 4: 添加默认头像图片**

需要添加一个默认头像图片到 `static/img/default-avatar.png`。如果不存在，可以创建一个占位图片或使用网络图片。

- [ ] **Step 5: 提交**

```bash
git add templates/personal.html static/js/personal.js static/css/personal.css
git commit -m "feat(profile): 重写个人中心页面，支持编辑资料和修改密码"
```

---

## Task 9: 验证功能完整性

**Files:**
- None

- [ ] **Step 1: 运行 Django 开发服务器测试**

```bash
cd D:/PycharmProjects/poetry_system
python manage.py runserver
```

- [ ] **Step 2: 测试注册功能**
1. 访问 `http://localhost:8000/users/register/`
2. 输入12位学号
3. 输入符合要求的密码
4. 选择安全问题并填写答案
5. 点击注册，确认成功跳转

- [ ] **Step 3: 测试登录功能**
1. 访问 `http://localhost:8000/users/login/`
2. 输入注册的学号和密码
3. 测试"记住我"功能
4. 确认登录成功跳转

- [ ] **Step 4: 测试个人中心**
1. 访问 `http://localhost:8000/users/profile/`
2. 检查用户信息显示是否正确
3. 测试编辑资料功能
4. 测试修改密码功能

- [ ] **Step 5: 测试退出登录**
1. 点击退出登录按钮
2. 确认跳转到首页
3. 再次访问个人中心，应跳转到登录页

- [ ] **Step 6: 测试密码重置**
1. 访问 `http://localhost:8000/users/reset-password/`
2. 输入学号
3. 回答安全问题
4. 设置新密码
5. 用新密码登录确认成功

---

## 完成检查清单

- [ ] User 模型扩展完成并迁移
- [ ] 注册功能添加安全问题
- [ ] 登录功能添加"记住我"
- [ ] 退出登录功能正常
- [ ] 修改密码功能正常
- [ ] 密码重置功能正常
- [ ] 个人中心显示真实用户信息
- [ ] 个人中心支持编辑资料
- [ ] 所有 AJAX 请求正确处理重定向
- [ ] CSRF token 正确配置
