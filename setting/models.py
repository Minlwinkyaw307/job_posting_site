from django.contrib.auth.models import User
from django.db import models
from ckeditor.fields import RichTextField
from django.utils import timezone
# from job.models import City
from django import forms


# from django.contrib.auth.models import AbstractUser


# Create your models here.
from django.utils.safestring import mark_safe


class Setting(models.Model):
    title = models.CharField(max_length=150, null=False, blank=False)
    keywords = models.CharField(max_length=150, null=False, blank=False)
    description = models.CharField(max_length=150, null=False, blank=False)
    company = models.CharField(max_length=50, verbose_name='Company Name', null=False, blank=False)
    address = models.TextField(verbose_name="Company's Address", null=False, blank=False)
    phone = models.CharField(max_length=20, null=False, blank=False)
    fax = models.CharField(max_length=20, null=False, blank=False)
    email = models.CharField(max_length=25, null=False, blank=False)
    smtpserver = models.CharField(max_length=35, verbose_name='SMTP Server', null=False, blank=False)
    smtpemail = models.CharField(max_length=25, verbose_name='SMTP Email', null=False, blank=False)
    smtppassword = models.CharField(max_length=100, verbose_name='SMTP Password', null=False, blank=False)
    smtpport = models.IntegerField(verbose_name='SMTP Port No.', null=False, blank=False)

    facebook = models.URLField(max_length=35, verbose_name='Facebook Link', null=False, blank=False)
    twitter = models.URLField(max_length=35, verbose_name='Twitter Link', null=False, blank=False)
    instagram = models.URLField(max_length=35, verbose_name='Instagram Link', null=False, blank=False)
    aboutus = RichTextField(verbose_name='About Us', null=False, blank=False)
    contactus = RichTextField(verbose_name='Contact Us', null=True, blank=True)
    references = RichTextField(verbose_name='References', null=True, blank=True)

    def __str__(self):
        return str(self.title)


faq_status = (
    ('New', 'New'),
    ('Answered', 'Answered'),
    ('Rejected', 'Rejected'),

)


class FAQ(models.Model):
    question = models.TextField(null=False, blank=True, )
    answer = models.TextField(null=False, blank=True, )
    status = models.CharField(max_length=15, choices=faq_status, default='New', null=False, blank=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.question)

    class Meta:
        ordering = ['id', 'updated_at', 'created_at', ]
        verbose_name = "FAQ"
        verbose_name_plural = "FAQ(s)"


# class FAQStatus(models.Model):
#     status = models.CharField(max_length=20, null=False, blank=False, )
# 
#     def __str__(self):
#         return str(self.status)
# 
#     class Meta:
#         verbose_name_plural = 'FAQ\'s Statuses'
#         verbose_name = "FAQ's Status"


message_status = (
    ('New', 'New'),
    ('Read', 'Read'),
    ('Reject', 'Reject'),
)


class ContactMessage(models.Model):
    first_name = models.CharField(max_length=30, null=False, blank=False)
    last_name = models.CharField(max_length=30, null=False, blank=False)
    subject = models.CharField(max_length=100, null=False, blank=False, default='')
    email = models.EmailField(null=False, blank=False, default='')
    message = models.TextField(null=False, blank=False)
    ip = models.GenericIPAddressField(null=True, blank=True)
    status = models.CharField(max_length=15, choices=message_status, default='New', null=False, blank=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return self.subject


applicant_status = (
    (True, 'Active'),
    (False, 'Deactivated'),
)


class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    profile = models.ImageField(upload_to='images/', default="images/profile.png")
    city = models.CharField(max_length=100, null=True, blank=True)
    university = models.CharField(max_length=100, null=True, blank=True)
    previous_company = models.CharField(max_length=100, null=True, blank=True)
    year_of_experience = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.user.username

    @property
    def email(self):
        return self.user.email

    @property
    def profile_image(self):
        return mark_safe(f'<img src="{self.profile.url}" height="50">')
