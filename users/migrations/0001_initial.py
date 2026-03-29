# Migration for custom User model with extra fields
# Manually created to match SQL schema modifications
# Date: 2026-03-28

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        # No dependencies - this is the first migration for users app
    ]

    operations = [
        # Add extra fields to User model (matching SQL ALTER TABLE commands)
        migrations.AddField(
            model_name='user',
            name='nickname',
            field=models.CharField(max_length=50, blank=True, default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='avatar',
            field=models.CharField(max_length=255, blank=True, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='bio',
            field=models.TextField(blank=True, default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='security_question',
            field=models.CharField(
                max_length=20,
                blank=True,
                choices=[
                    ('mother_name', '您母亲的姓名是？'),
                    ('birth_city', '您的出生城市是？'),
                    ('first_school', '您的第一所学校名称是？'),
                    ('favorite_book', '您最喜欢的书籍是？'),
                ],
            ),
        ),
        migrations.AddField(
            model_name='user',
            name='security_answer',
            field=models.CharField(max_length=100, blank=True, default=''),
            preserve_default=False,
        ),
    ]
