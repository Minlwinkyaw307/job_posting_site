from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from django.urls import reverse

job_types = (
    ('Full-Time', 'Full-Time'),
    ('Full-Time', 'Full-Time'),
)
gender_type = (
    ('male', 'Male'),
    ('female', 'female'),
    ('any', 'Any'),
)


class Job(models.Model):
    title = models.CharField(max_length=150, null=False, blank=False)
    slug = models.CharField(max_length=150, unique=True, null=False, blank=False)
    keywords = models.CharField(max_length=150, null=False, blank=False)

    company_name = models.CharField(max_length=50, null=False, blank=False, default="Unknown")
    city = models.CharField(max_length=50, null=False, blank=False, default="Unknown")
    company_logo = models.ImageField(upload_to='images/', default="images/no-logo.png")

    category = models.ForeignKey('Category', on_delete=models.CASCADE, null=False, blank=False)
    job_type = models.CharField(max_length=50, choices=job_types, null=False, blank=False, default='full-time')
    gender = models.CharField(max_length=50, choices=gender_type, null=False, blank=False, default='any')
    experience = models.CharField(max_length=50, null=False, blank=False, default='At Least 1 Year')
    salary = models.IntegerField(null=False, blank=False, default=0)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,verbose_name='Managed By', null=True, blank=False, default=None)

    description = RichTextField(verbose_name='Job Description', null=False, blank=False)
    responsibilities = RichTextField(verbose_name='Job Responsibilities', null=True, blank=True)
    education = RichTextField(verbose_name='Education And Requirements', null=True, blank=True)
    benefits = RichTextField(verbose_name='Other Benefits', null=True, blank=True)
    deadline = models.DateTimeField(default=timezone.now)

    thumbnail = models.ImageField(upload_to='images/', default="images/broken-image.gif")
    status = models.BooleanField(default=False, null=False, blank=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    @property
    def images(self):
        return Image.objects.filter(job=self)

    def get_absolute_url(self):
        return reverse('job.detail', args=[str(self.slug), ])

    def __str__(self):
        return f'{self.title}'


class Image(models.Model):
    job = models.ForeignKey('Job', on_delete=models.CASCADE, default=None, null=True, blank=False)
    title = models.CharField(max_length=150, null=False, blank=False)
    image = models.ImageField(upload_to='images/', default="images/no-image.png")

    def __str__(self):
        return f'{self.title}'


class Category(models.Model):
    parent = models.ForeignKey('Category', on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=150, null=False, blank=False)
    slug = models.CharField(max_length=150, unique=True, null=False, blank=False)
    keywords = models.CharField(max_length=150, null=False, blank=False)
    description = models.CharField(max_length=150, null=False, blank=False)
    image = models.ImageField(upload_to='images/')
    status = models.BooleanField(default=False, null=False, blank=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name_plural = 'Categories'


# class GeneralStatus(models.Model):
#     status = models.CharField(max_length=25, blank=False, null=False, )
#
#     def __str__(self):
#         return str(self.status)
#
#     class Meta:
#         verbose_name_plural = 'Category Statuses'


class Comment(models.Model):
    comment = models.TextField(blank=False, null=False, )
    rate = models.IntegerField(blank=False, null=False, )
    job = models.ForeignKey('Job', on_delete=models.CASCADE, blank=False, null=False, )
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False, )
    ip = models.GenericIPAddressField(null=False, blank=False)
    status = models.BooleanField(default=False, null=False, blank=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

# class Orders(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
#     name = models.CharField(max_length=25, null=False, blank=False)
#     surname = models.CharField(max_length=25, null=False, blank=False)
#     phone = models.CharField(max_length=20, null=False, blank=False)
#     address = models.TextField(null=False, blank=False)
#     email = models.EmailField(null=False, blank=False)
#     total = models.FloatField(null=False, blank=False)
#     note = models.TextField(null=False, blank=False)
#     ip = models.GenericIPAddressField(null=False, blank=False)
#     created_at = models.DateTimeField(default=timezone.now)
#     updated_at = models.DateTimeField(default=timezone.now)
# 
# 
# class OrderStatus(models.Model):
#     status = models.CharField(max_length=25, blank=False, null=False, )
