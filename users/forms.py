from django import forms


class RegisterForm(forms.Form):
    username = forms.CharField(min_length=12, max_length=12, required=True,
                               error_messages={
                                   'min_length': '用户名最小长度为12位',
                                   'max_length': '用户名最大长度为12位',
                               })

    password = forms.CharField(min_length=8, max_length=20, required=True,
                               error_messages={
                                   'min_length': '密码最小长度为8',
                                   'max_length': '密码最大长度为20'
                               })

    password2 = forms.CharField(min_length=8, max_length=20, required=True,
                                error_messages={
                                    'min_length': '密码最小长度为8',
                                    'max_length': '密码最大长度为20',
                                })

    # 使用全局钩子验证两次密码是否一致
    def clean(self):
        clean_data = super().clean()
        password = clean_data.get('password')
        password2 = clean_data.get('password2')
        if password != password2:
            raise forms.ValidationError('输入的两次密码不一致')
        return clean_data


class LoginForm(forms.Form):
    username = forms.CharField(max_length=12, min_length=12)
    password = forms.CharField(max_length=20, min_length=8)
    # 是否记住密码
    remembered = forms.BooleanField(required=False)
