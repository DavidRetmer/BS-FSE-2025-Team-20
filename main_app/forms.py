from django.forms import ModelForm
from django import forms 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username' ,'email' ,'password1','password2']

class SendMailForm(forms.Form):
    title = forms.CharField(label="put our mail here",max_length=200)
    

class ContactForm(forms.Form):
    title = forms.CharField(label="put our mail here",max_length=200)
    description = forms.CharField(label="descrive ur problem here :" ,widget=forms.Textarea)  