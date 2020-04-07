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
