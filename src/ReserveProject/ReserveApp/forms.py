from django import forms
from .models import User

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['userName', 'blood', 'mail', 'password', 'entryDate',  'masterMode']