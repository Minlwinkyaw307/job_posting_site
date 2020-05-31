from django.contrib import admin
from .models import *
from django.utils import timezone
from job_posting_site.settings import MEDIA_ROOT, BASE_DIR
import os


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    readonly_fields = ['job', 'applicant', 'created_at', 'updated_at']
    search_fields = ('id', 'applicant__username', 'job__title')
    list_display = ('job', 'applicant', 'status', 'ip', 'updated_at')
    list_editable = ['status', ]
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


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'parent', 'status', 'created_at', 'updated_at')
    search_fields = ('id', 'title', 'parent__title')
    list_editable = ('status',)
    list_filter = ('status', 'parent', 'created_at',)

    def render_change_form(self, request, context, *args, **kwargs):
        context['adminform'].form.fields['parent'].queryset = Category.objects.filter(parent=None)
        return super(CategoryAdmin, self).render_change_form(request, context, *args, **kwargs)

    def save_model(self, request, obj, form, change):
        obj.updated_at = timezone.now()
        obj.save()

    def delete_model(self, request, obj):
        obj.image.delete()
        obj.delete()


admin.site.register(City)
admin.site.register(Comment)


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['title', 'job']
    list_filter = ('job', 'title')
    search_fields = ('title', 'job__title')

    def delete_model(self, request, obj):
        obj.image.delete()
        obj.delete()

class JobInlineImage(admin.StackedInline):
    model = Image
    extra = 2

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    readonly_fields = ['created_by', 'updated_at']
    list_filter = ('title', 'category',)
    list_editable = ('status',)
    inlines = [JobInlineImage]
    search_fields = ('title', 'category__title', 'city__name', 'id')
    # fieldsets = (
    #     ('Basic', {
    #         'fields': ('title', 'keywords', 'slug',)
    #     }),
    #     JobInlineImage
    #     ('Company Information', {
    #         'fields': ('company_name', 'city', 'company_logo', 'created_by'),
    #     }),
    #     ('Job Info', {
    #         'fields': ('category', 'job_type', 'gender', 'salary')
    #     }),
    #     ('More Detail', {
    #         'fields': ('description', 'responsibilities', 'education', 'benefits', 'deadline')
    #     }),
    #     ('Other', {
    #         'fields': ('thumbnail', 'status', 'created_at', 'updated_at')
    #     }),
    # )
    list_display = ('title', 'category', 'city', 'salary', 'status')
    list_filter = ('category', 'salary', 'created_at')

    def save_model(self, request, obj, form, change):
        obj.created_by = request.user
        obj.updated_at = timezone.now()
        obj.save()

    def render_change_form(self, request, context, *args, **kwargs):
        context['adminform'].form.fields['category'].queryset = Category.objects.exclude(parent=None)
        return super(JobAdmin, self).render_change_form(request, context, *args, **kwargs)

    def delete_model(self, request, obj):
        if obj.company_logo.url != 'images/no-logo.png':
            obj.company_logo.delete()
        if obj.thumbnail.url != 'images/broken-image.gif':
            obj.thumbnail.delete()
        obj.delete()


@admin.register(Saved)
class SavedAdmin(admin.ModelAdmin):
    readonly_fields = ['job', 'applicant', 'created_at']
    search_fields = ('id', 'job__title', 'applicant__username', 'ip')
    list_display = ('job', 'applicant', 'created_at', 'ip')
    list_filter = ('job', 'applicant', 'created_at')
    fieldsets = (
        ('Main Info', {
            'fields': ('job', 'applicant',)
        }),
        ('Other Info', {
            'fields': ('created_at',),
        }),
    )

