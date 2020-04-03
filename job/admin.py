from django.contrib import admin
from .models import *


# Register your models here.


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Basic', {
            'fields': ('title', 'keywords', 'slug',)
        }),
        ('Company Information', {
            'fields': ('company_name', 'city', 'company_logo'),
        }),
        ('Job Info', {
            'fields': ('category', 'job_type', 'gender', 'salary', 'created_by')
        }),
        ('More Detail', {
            'fields': ('description', 'responsibilities', 'education', 'benefits', 'deadline')
        }),
        ('Other', {
            'fields': ('thumbnail', 'status', 'created_at', 'updated_at')
        }),
    )
    list_display = ('id', 'title', 'category', 'salary', 'status')
    list_filter = ('category', 'salary', 'updated_at')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'parent', 'status')
    list_filter = ('status', 'parent')


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    pass


# @admin.register(Orders)
# class OrdersAdmin(admin.ModelAdmin):
#     list_display = ('title', 'category', 'price', 'status')
