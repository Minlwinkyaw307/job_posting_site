from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import *
from ckeditor.fields import RichTextField
from .models import *
from setting.models import *


# class ImageForm(forms.ModelForm):
#     class Meta:
#         model = Image
#         fields = ['title', 'image']


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = {'first_name', 'last_name', 'email', 'username', 'password1', 'password2'}

        widgets = {
            'first_name': TextInput(
                attrs={'class': 'form-control', 'placeholder': 'First Name', 'help_text': 'Optional'}),
            'last_name': TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Last Name', 'help_text': 'Optional'}),
            'email': TextInput(attrs={'class': 'form-control', 'placeholder': 'Email',
                                      'help_text': 'Optional'}),
            'username': TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Full Name', 'help_text': 'Optional'}),
            'password1': TextInput(attrs={'class': 'form-control', 'placeholder': 'Password',
                                          'help_text': 'Optional'}),
            'password2': TextInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password',
                                          'help_text': 'Optional'}),
        }


class ContactForm(forms.ModelForm):
    field_order = ['first_name', 'last_name', 'email', 'subject', 'message']

    class Meta:
        model = ContactMessage
        fields = {'message', 'last_name', 'email', 'subject', 'first_name', }
        widgets = {
            'first_name': TextInput(
                attrs={'class': 'form-control', 'placeholder': 'First Name', 'help_text': 'Optional'}),
            'last_name': TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Last Name', 'help_text': 'Optional'}),
            'email': TextInput(attrs={'class': 'form-control', 'placeholder': 'Email',
                                      'help_text': 'Optional'}),
            'subject': TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Subject', 'help_text': 'Optional'}),
            'message': Textarea(
                attrs={'class': 'form-control', 'cols': "30", 'rows': "7",
                       'placeholder': 'Write your notes or questions here...', 'help_text': 'Optional'}),

        }
