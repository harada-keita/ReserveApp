from django.conf import settings
from django.db import models
from django.utils import timezone

class User(models.Model):
    userName = models.CharField("名前", max_length=30)
    BloodType = [('a', 'A'), ('b', 'B'), ('o', 'O'), ('ab', 'AB')]
    blood = models.CharField("血液型", max_length=2, choices=BloodType, default='b')
    # EmailFieldは文字列に「@」がないとエラー
    mail = models.EmailField("メールアドレス")
    password = models.CharField("パスワード", max_length=30, default="0000", null=False)
    entryDate = models.DateTimeField("登録日", default=timezone.now)
    masterMode = models.BooleanField("管理者", default=False)