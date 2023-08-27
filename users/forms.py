from django import forms
from django.forms import Form
from django.contrib.auth.forms import UserChangeForm
from .models import User


class CustomUserCreationForm(forms.ModelForm):
    email = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = '__all__'

    def save(self, commit=True):
        user = super(CustomUserCreationForm, self)
        user.username = self.cleaned_data.get('username')
        user.first_name = self.cleaned_data.get('first_name')
        user.father_name = self.cleaned_data.get('father_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.username = self.cleaned_data.get('username')
        user.email = self.cleaned_data.get('email')
        user.is_staff = self.cleaned_data.get('is_staff')
        user.phone = self.cleaned_data.get('phone')
        user.gender = self.cleaned_data.get('gender')
        
        # user.is_active = self.cleaned_data.get('is_active')
        user.is_enabled = self.cleaned_data.get('is_enabled')
        user.is_superuser = self.cleaned_data.get('is_superuser')
        user.set_password(self.cleaned_data.get('password'))        

        if commit:
            user.save()
            
        return user


class CustomUserChangeForm(UserChangeForm):
    email = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = '__all__'


class LoginForm(Form):
    class Meta(Form):
        model = User
        fields = ['username', 'password']

