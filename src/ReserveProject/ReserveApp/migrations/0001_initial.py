# Generated by Django 5.1.6 on 2025-06-24 15:12

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userName', models.CharField(max_length=30, verbose_name='名前')),
                ('blood', models.CharField(choices=[('a', 'A'), ('b', 'B'), ('o', 'O'), ('ab', 'AB')], default='b', max_length=2, verbose_name='血液型')),
                ('mail', models.EmailField(max_length=254, verbose_name='メールアドレス')),
                ('password', models.CharField(default='0000', max_length=30, verbose_name='パスワード')),
                ('entryDate', models.DateTimeField(default=django.utils.timezone.now, verbose_name='登録日')),
                ('masterMode', models.BooleanField(default=False, verbose_name='管理者')),
            ],
        ),
    ]
