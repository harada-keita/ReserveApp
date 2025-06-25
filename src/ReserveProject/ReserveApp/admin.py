from django.contrib import admin
from .models import User

# Register your models here.
#ここにモデルを追加することによりhttp://localhost:8000/admin/の管理者サイトで編集することが可能となる
admin.site.register(User)