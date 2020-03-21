from django.contrib.auth.models import User
from django import forms


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_pass = forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField(max_length=200, help_text='Required')
    #confirmation_token = forms.CharField()

    class Meta:
        model = User
        fields = ('username', 'email', 'password')
