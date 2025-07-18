from django import forms
from .models import User

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['userName', 'blood', 'mail', 'password', 'entryDate',  'masterMode']
        
class UserDBForm(forms.Form):
    userName = forms.CharField(label='ユーザー名')# ここのlabelは検索のためのテキストボックスのラベル（テキストボックスの前に書かれる）
    
    
class UserCreateForm(forms.Form):
    class Meta:
        model = User
        fields = ['userName', 'blood', 'mail', 'password', 'entryDate',  'masterMode']