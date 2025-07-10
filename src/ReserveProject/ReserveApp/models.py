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
    
    def __str__(self):
        if self.masterMode == True:
            masterStr = '管理者'
        else:
            masterStr = '一般'
        return self.userName + '（' + masterStr + '）'
    
class Place(models.Model):
    name = models.CharField('場所名', max_length=255)
    price = models.IntegerField('1時間当たりの値段')
    user = models.ForeignKey(User, verbose_name='予約者', on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name
    
class Schedule(models.Model):
    #予約スケジュール
    start = models.DateTimeField('開始時間')
    end = models.DateTimeField('終了時間')
    name = models.CharField('予約者名', max_length=255)
    #以下のForeignKeyは他のモデルとつなげる
    user = models.ForeignKey(User, verbose_name='予約者', on_delete=models.CASCADE)