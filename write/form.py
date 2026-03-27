from django import forms
from .models import Poem  # 从 models 模块导入 Poem 模型

class PoetryForm(forms.ModelForm):  # 继承自 ModelForm
    class Meta:
        model = Poem  # 指定关联的模型
        fields = ['poet_name', 'poetry_name', 'poetry_content']  # 指定要包含的字段
