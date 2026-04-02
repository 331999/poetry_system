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
    email = forms.EmailField(
        required=False,
        error_messages={
            'invalid': '请输入有效的邮箱地址',
        }
    )

    class Meta:
        model = User
        fields = ['nickname', 'email', 'avatar', 'bio']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 3, 'maxlength': 500}),
        }
        error_messages = {
            'nickname': {'max_length': '昵称最长50个字符'},
            'bio': {'max_length': '个人简介最长500个字符'},
        }

    def clean_email(self):
        email = self.cleaned_data.get('email', '')
        if email:
            import re
            pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(pattern, email):
                raise forms.ValidationError('请输入有效的邮箱地址，格式应为 xxx@xxx.xxx')
        return email
