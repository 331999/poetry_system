# 用户认证系统完善设计方案

## 概述

完善古诗词鉴赏网的登录注册系统，修复现有问题并添加密码重置、用户信息扩展等功能。

## 需求

### 功能需求

| 功能 | 详情 |
|------|------|
| 修复现有功能 | 退出登录、修改密码、记住我 |
| 密码重置 | 通过安全问题重置密码 |
| 用户扩展字段 | 昵称、头像、个人简介 |
| 个人中心 | 显示真实用户信息，支持编辑 |

### 非功能需求

- 不需要登录失败保护机制
- 头像上传到本地 media 目录
- 安全问题只支持一组

## 架构设计

### 数据模型

扩展 `users/models.py` 中的 User 模型：

```python
# 安全问题选项
SECURITY_QUESTIONS = [
    ('mother_name', '您母亲的姓名是？'),
    ('birth_city', '您的出生城市是？'),
    ('first_school', '您的第一所学校名称是？'),
    ('favorite_book', '您最喜欢的书籍是？'),
]

class User(AbstractUser):
    nickname = models.CharField('昵称', max_length=50, blank=True, default='')
    avatar = models.ImageField('头像', upload_to='avatars/', blank=True, null=True)
    bio = models.TextField('个人简介', max_length=500, blank=True, default='')
    security_question = models.CharField('安全问题', max_length=20, blank=True, choices=SECURITY_QUESTIONS)
    security_answer = models.CharField('安全问题答案', max_length=100, blank=True)  # 存储小写哈希值

    class Meta:
        db_table = 'user'
        verbose_name = '用户'
        verbose_name_plural = '用户'
```

### API 端点

| 端点 | 方法 | 功能 | 状态 |
|------|------|------|------|
| `/users/register/` | GET/POST | 用户注册 | 已有，需修复 |
| `/users/login/` | GET/POST | 用户登录 | 已有，需修复 |
| `/users/logout/` | POST | 退出登录 | 新增 |
| `/users/profile/` | GET/PUT | 个人信息查看/修改 | 重构 |
| `/users/change-password/` | POST | 修改密码 | 新增 |
| `/users/reset-password/` | GET/POST | 密码重置 | 新增 |
| `/users/check-username/` | GET | 检查用户名是否存在 | 已有 |

## 功能详细设计

### 1. 注册流程

**现有问题**：
- AJAX 成功后未正确处理重定向
- 无安全问题设置

**改进**：
1. 注册表单添加安全问题选择和答案输入
2. 后端返回 JSON 响应，前端根据响应处理重定向
3. 安全问题选项（预定义选择框）：
   - 您母亲的姓名是？
   - 您的出生城市是？
   - 您的第一所学校名称是？
   - 您最喜欢的书籍是？
4. 安全答案存储时转换为小写，验证时忽略大小写比较

### 2. 登录流程

**现有问题**：
- "记住我" 功能未实现
- AJAX 成功后未正确处理重定向

**改进**：
1. 实现"记住我"功能：
   - 选中：session 有效期 7 天
   - 未选中：session 浏览器关闭失效
2. 返回 JSON 响应，包含重定向 URL

### 3. 退出登录

**新增功能**：
```python
class Logout(View):
    def post(self, request):
        logout(request)
        response = redirect('index')
        response.delete_cookie('username')
        return JsonResponse({'code': 200, 'msg': '退出成功'})
```

### 4. 修改密码

**新增功能**：
```python
class ChangePassword(View):
    def post(self, request):
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')

        if not request.user.check_password(old_password):
            return JsonResponse({'code': 400, 'msg': '旧密码错误'})

        request.user.set_password(new_password)
        request.user.save()
        logout(request)
        return JsonResponse({'code': 200, 'msg': '密码修改成功'})
```

### 5. 密码重置（安全问题）

**流程**：
1. 用户输入学号
2. 系统显示该用户设置的安全问题
3. 用户输入答案
4. 验证正确后，允许设置新密码

**视图设计**：
```python
class ResetPassword(View):
    def get(self, request):
        username = request.GET.get('username')
        try:
            user = User.objects.get(username=username)
            return JsonResponse({
                'code': 200,
                'question': user.security_question
            })
        except User.DoesNotExist:
            return JsonResponse({'code': 404, 'msg': '用户不存在'})

    def post(self, request):
        username = request.POST.get('username')
        answer = request.POST.get('answer')
        new_password = request.POST.get('new_password')

        user = User.objects.get(username=username)
        # 答案比较时忽略大小写
        if user.security_answer.lower() != answer.lower():
            return JsonResponse({'code': 400, 'msg': '答案错误'})

        user.set_password(new_password)
        user.save()
        return JsonResponse({'code': 200, 'msg': '密码重置成功'})
```

### 6. 个人中心

**现有问题**：
- 学号硬编码
- 无登录状态检查
- 修改密码功能不工作

**改进**：
1. 使用 Django 模板变量显示真实用户信息
2. 添加 `@login_required` 装饰器或 LoginRequiredMixin
3. 支持编辑昵称、头像、简介
4. 将修改密码功能独立到单独 API

## 前端设计

### loginRegister.html 改动

1. 注册表单添加安全问题选择器和答案输入框
2. 登录表单添加"记住我"复选框
3. 添加"忘记密码"链接
4. 修复 AJAX 响应处理，正确重定向

### personal.html 改动

1. 使用 `{{ user.nickname }}` 或 `{{ user.username }}` 显示用户名
2. 使用 `{{ user.avatar.url }}` 显示头像
3. 添加编辑个人信息的模态框
4. 添加退出登录按钮功能

### resetPassword.html 新增

```html
<!-- 密码重置页面 -->
<div class="reset-container">
    <input type="text" id="username" placeholder="请输入学号">
    <button id="getQuestion">获取安全问题</button>

    <div id="questionSection" style="display:none">
        <p id="securityQuestion"></p>
        <input type="text" id="answer" placeholder="请输入答案">
        <input type="password" id="newPassword" placeholder="新密码">
        <button id="resetBtn">重置密码</button>
    </div>
</div>
```

## 配置改动

### settings.py

```python
# 添加 media 配置
import os
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Session 配置
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
SESSION_COOKIE_AGE = 60 * 60 * 24 * 7  # 7 天
```

### urls.py (主项目)

```python
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # ...existing patterns...
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

## 文件改动清单

| 文件 | 改动类型 | 内容 |
|------|----------|------|
| `users/models.py` | 修改 | 添加 nickname, avatar, bio, security_question, security_answer 字段 |
| `users/views.py` | 修改 | 添加 Logout, ChangePassword, ResetPassword 视图；修改 Login, Register, Person |
| `users/urls.py` | 修改 | 添加新路由 |
| `users/forms.py` | 修改 | 添加新表单类 |
| `users/admin.py` | 修改 | 添加新字段到 admin |
| `templates/loginRegister.html` | 修改 | 添加安全问题和记住我 |
| `templates/personal.html` | 重写 | 显示真实用户信息，编辑功能 |
| `templates/resetPassword.html` | 新增 | 密码重置页面 |
| `static/js/loginRegister.js` | 修改 | 修复 AJAX 响应处理 |
| `static/js/personal.js` | 重写 | 实现个人信息编辑 |
| `static/js/resetPassword.js` | 新增 | 密码重置逻辑 |
| `poetry_system/settings.py` | 修改 | 添加 media 配置 |
| `poetry_system/urls.py` | 修改 | 添加 media 路由 |

## 数据库迁移

执行以下命令创建并应用迁移：

```bash
python manage.py makemigrations users
python manage.py migrate
```

## 测试要点

1. 注册流程：安全问题是否正确保存
2. 登录流程：记住我是否生效
3. 退出登录：session 和 cookie 是否清除
4. 修改密码：旧密码验证、新密码复杂度
5. 密码重置：安全问题验证、密码更新
6. 个人中心：信息显示、编辑保存、头像上传
7. 权限控制：未登录访问个人中心跳转登录
