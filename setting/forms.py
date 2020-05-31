from django.contrib.auth.forms import UserChangeForm
from django.forms import *
from django.contrib import admin
from ckeditor.widgets import CKEditorWidget

from .models import *


class ProfileUserUpdateForm(UserChangeForm):
    password = None
    field_order = ['username', 'first_name', 'last_name', ]

    class Meta:
        model = User
        fields = {'username', 'first_name', 'last_name', }
        widgets = {
            'first_name': TextInput(
                attrs={'class': 'form-control', 'placeholder': 'First Name',
                       'help_text': 'Optional'}),
            'last_name': TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Last Name',
                       'help_text': 'Optional'}),
            'username': TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Username',
                       'help_text': 'Optional'}),
            # 'date_joined': TextInput(
            #     attrs={'class': 'form-control', 'disabled': 'true', }),
            # 'last_login': TextInput(
            #     attrs={'class': 'form-control', 'disabled': 'true', }),
        }


class CustomerProfileUpdateForm(forms.ModelForm):
    field_order = ['city', 'university', 'previous_company', 'year_of_experience']
    class Meta:
        model = Customer
        fields = {'city', 'university', 'previous_company', 'year_of_experience'}
        widgets = {
            'city': TextInput(
                attrs={'class': 'form-control', 'placeholder': 'City',
                       'help_text': 'Optional'}),
            'university': TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Graduated University',
                       'help_text': 'Optional'}),
            'previous_company': TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Previous Company',
                       'help_text': 'Optional'}),
            'year_of_experience': TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Year of Experience', 'type': 'number',
                       'help_text': 'Optional'}),
        }


class FAQForm(forms.ModelForm):
    class Meta:
        model = FAQ
        fields = {'question', }
        widgets = {
            'question': Textarea(
                attrs={'class': 'form-control', 'placeholder': 'Please Enter Your Question', 'cols': '20', 'rows': '5'})
        }


class ChangeProfileForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = {'profile', }
        widgets = {
            'question': Textarea(
                attrs={'class': 'form-control-file', }, )
        }
