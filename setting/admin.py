from django.contrib import admin
from .models import *


# Register your models here.

@admin.register(Setting)
class SettingAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Basic', {
            'fields': ('title', 'keywords', 'description',)
        }),
        ('Company Information', {
            # 'classes': ('collapse',),
            'fields': ('company', 'address', 'phone', 'email', 'fax'),
        }),
        ('SMTP', {
            'fields': ('smtpserver', 'smtpemail', 'smtppassword', 'smtpport')
        }),
        ('Social Media Links', {
            'fields': ('facebook', 'twitter', 'instagram',)
        }),
        ('About Us Page', {
            'fields': ('aboutus',)
        }),
    )
    list_display = ['title', 'company', 'email', ]


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ['question', 'status', 'created_at', ]



