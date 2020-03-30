from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


# Create your models here.
class Job(models.Model):
    title = models.CharField(max_length=150, null=False, blank=False)
    slug = models.CharField(max_length=150, unique=True, null=False, blank=False)
    keywords = models.CharField(max_length=150, null=False, blank=False)
    description = models.CharField(max_length=150, null=False, blank=False)
    image = models.ManyToManyField('Image', default=[1])
    category = models.ForeignKey('Category', on_delete=models.CASCADE, null=False, blank=False)
    detail = models.TextField(null=False, blank=False)
    price = models.FloatField(null=False, blank=False, default=0)
    amount = models.FloatField(null=False, blank=False, default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    status = models.ForeignKey('JobStatus', on_delete=models.SET_DEFAULT, null=False, blank=False, default=1)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.title}'


class Image(models.Model):
    # job = models.ForeignKey('Job', on_delete=models.CASCADE, null=False, blank=False)
    title = models.CharField(max_length=150, null=False, blank=False)
    image = models.ImageField(upload_to='images/', default="images/broken-image.gif")

    def __str__(self):
        return f'{self.title}'


class JobStatus(models.Model):
    status = models.CharField(max_length=25, blank=False, null=False, )

    def __str__(self):
        return str(self.status)

    class Meta:
        verbose_name_plural = 'Job Statuses'


class Category(models.Model):
    parent = models.ForeignKey('Category', on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=150, null=False, blank=False)
    keywords = models.CharField(max_length=150, null=False, blank=False)
    description = models.CharField(max_length=150, null=False, blank=False)
    image = models.ImageField(upload_to='images/')
    status = models.ForeignKey('JobStatus', on_delete=models.SET_DEFAULT, null=False, blank=False, default=1)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    slug = models.CharField(max_length=150, unique=True, null=False, blank=False)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name_plural = 'Categories'


class GeneralStatus(models.Model):
    status = models.CharField(max_length=25, blank=False, null=False, )

    def __str__(self):
        return str(self.status)

    class Meta:
        verbose_name_plural = 'Category Statuses'
        
        
class Comment(models.Model):
    comment = models.TextField(blank=False, null=False,)
    rate = models.IntegerField(blank=False, null=False,)
    job = models.ForeignKey('Job', on_delete=models.CASCADE, blank=False, null=False,)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False,)
    ip = models.GenericIPAddressField(null=False, blank=False)
    status = models.ForeignKey(GeneralStatus, on_delete=models.CASCADE, blank=False, null=False, )
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
