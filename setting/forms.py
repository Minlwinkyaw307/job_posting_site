from django import forms
from django.contrib import admin
from ckeditor.widgets import CKEditorWidget

from .models import Setting


class SettingAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Setting


class PostAdmin(admin.ModelAdmin):
    form = SettingAdminForm
