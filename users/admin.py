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
