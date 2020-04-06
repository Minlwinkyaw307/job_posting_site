from django.contrib import admin
from .models import *
from django.utils import timezone


# Register your models here.
@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    pass


@admin.register(Saved)
class SavedAdmin(admin.ModelAdmin):
    readonly_fields = ['job', 'applicant', 'created_at']
    list_display = ('job', 'applicant', 'created_at')
    list_filter = ('job', 'applicant', 'created_at')
    fieldsets = (
        ('Main Info', {
            'fields': ('job', 'applicant',)
        }),
        ('Other Info', {
            'fields': ('created_at',),
        }),
    )


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    readonly_fields = ['job', 'applicant', 'created_at']
    list_display = ('job', 'applicant', 'status', 'updated_at')
    list_filter = ('job', 'applicant', 'updated_at')
    fieldsets = (
        ('Main Info', {
            'fields': ('job', 'applicant', 'status')
        }),
        ('Other Info', {
            'fields': ('created_at', 'updated_at'),
        }),
    )

    def save_model(self, request, obj, form, change):
        obj.updated_at = timezone.now()
        obj.save()


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    readonly_fields = ['created_by']
    fieldsets = (
        ('Basic', {
            'fields': ('title', 'keywords', 'slug',)
        }),
        ('Company Information', {
            'fields': ('company_name', 'city', 'company_logo', 'created_by'),
        }),
        ('Job Info', {
            'fields': ('category', 'job_type', 'gender', 'salary')
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

    def save_model(self, request, obj, form, change):
        obj.created_by = request.user
        obj.save()

    def render_change_form(self, request, context, *args, **kwargs):
        context['adminform'].form.fields['category'].queryset = Category.objects.exclude(parent=None)
        return super(JobAdmin, self).render_change_form(request, context, *args, **kwargs)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'parent', 'status')
    list_filter = ('status', 'parent')

    def render_change_form(self, request, context, *args, **kwargs):
        context['adminform'].form.fields['parent'].queryset = Category.objects.filter(parent=None)
        return super(CategoryAdmin, self).render_change_form(request, context, *args, **kwargs)


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    pass

# @admin.register(Orders)
# class OrdersAdmin(admin.ModelAdmin):
#     list_display = ('title', 'category', 'price', 'status')
