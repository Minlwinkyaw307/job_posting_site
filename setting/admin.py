from django.contrib import admin
from .models import *


# Register your models here.

@admin.register(ContactMessage)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['subject', 'full_name', 'email', 'ip', 'status']
    list_filter = ('email', 'status', 'created_at', 'updated_at')
    readonly_fields = ['full_name']
    list_editable = ('status',)
    search_fields = ('subject', 'first_name', 'last_name', 'email')
    pass


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['user', 'email', 'profile_image', 'city', 'university', 'year_of_experience', ]
    list_filter = ['city', 'university', 'user__date_joined', ]
    readonly_fields = ('profile_image', 'email')


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
        ('Page\'s Content', {
            'fields': ('aboutus', 'contactus', 'references')
        }),
    )
    list_display = ['title', 'company', 'email', ]


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ['question', 'status', 'created_at', ]
    list_editable = ('status',)
    list_filter = ['status', 'created_at', 'updated_at']
