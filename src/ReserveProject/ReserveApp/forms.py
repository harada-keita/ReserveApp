from django import forms
from .models import User



class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), label='パスワード')
    
    class Meta:
        model = User
        fields = ['username', 'blood', 'email', 'password', 'is_staff', 'is_superuser']
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])  # パスワードをハッシュ化
        if commit:
            user.save()
        return user




class UserDBForm(forms.Form):
    userName = forms.CharField(label='ユーザー名')# ここのlabelは検索のためのテキストボックスのラベル（テキストボックスの前に書かれる）
    

