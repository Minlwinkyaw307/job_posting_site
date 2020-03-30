from django.contrib import admin
from .models import *


# Register your models here.


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'price', 'status')
    list_filter = ('category', 'price', 'updated_at')


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
