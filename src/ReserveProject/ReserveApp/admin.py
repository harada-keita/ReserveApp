from django.contrib import admin
from .models import User, Place, Schedule

# Register your models here.
#ここにモデルを追加することによりhttp://localhost:8000/admin/の管理者サイトで編集することが可能となる
admin.site.register(User)
admin.site.register(Place)
admin.site.register(Schedule)