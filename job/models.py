from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from django.urls import reverse
from django.utils.safestring import mark_safe

from setting.models import Customer

job_types = (
    ('Full-Time', 'Full-Time'),
    ('Part-Time', 'Part-Time'),
)
gender_type = (
    ('male', 'Male'),
    ('female', 'female'),
    ('any', 'Any'),
)

job_status = (
    (True, 'Published'),
    (False, 'Unpublished'),
)


class Job(models.Model):
    title = models.CharField(max_length=150, null=False, blank=False)
    slug = models.CharField(max_length=150, unique=True, null=False, blank=False)
    keywords = models.CharField(max_length=150, null=False, blank=False)

    company_name = models.CharField(max_length=50, null=False, blank=False, default="Unknown")
    city = models.ForeignKey('City', on_delete=models.CASCADE, blank=False, null=False, default=1)
    company_logo = models.ImageField(upload_to='images/', default="images/no-logo.png")

    category = models.ForeignKey('Category', on_delete=models.CASCADE, null=False, blank=False)
    job_type = models.CharField(max_length=50, choices=job_types, null=False, blank=False, default='full-time')
    gender = models.CharField(max_length=50, choices=gender_type, null=False, blank=False, default='any')
    experience = models.CharField(max_length=50, null=False, blank=False, default='At Least 1 Year')
    salary = models.IntegerField(null=False, blank=False, default=0)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Managed By', null=True, blank=False,
                                   default=None)

    description = RichTextField(verbose_name='Job Description', null=False, blank=False)
    responsibilities = RichTextField(verbose_name='Job Responsibilities', null=True, blank=True)
    education = RichTextField(verbose_name='Education And Requirements', null=True, blank=True)
    benefits = RichTextField(verbose_name='Other Benefits', null=True, blank=True)
    deadline = models.DateTimeField(default=timezone.now)

    thumbnail = models.ImageField(upload_to='images/', default="images/broken-image.gif")
    status = models.BooleanField(choices=job_status, default=False, null=False, blank=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    @property
    def images(self):
        return Image.objects.filter(job=self)

    @property
    def thumbnail_image(self):
        return mark_safe(f'<img src="{self.thumbnail.url}" height="50">')

    @property
    def logo_image(self):
        return mark_safe(f'<img src="{self.company_logo.url}" height="50">')


    def get_absolute_url(self):
        return reverse('job.detail', args=[str(self.slug), ])

    def __str__(self):
        return f'{self.title}'


class City(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Cities'


class Image(models.Model):
    job = models.ForeignKey('Job', on_delete=models.CASCADE, default=None, null=True, blank=False)
    title = models.CharField(max_length=150, null=False, blank=False)
    image = models.ImageField(upload_to='images/', default="images/no-image.png")

    def __str__(self):
        return f'{self.title}'

    @property
    def image_tag(self):
        return mark_safe("<img src='{}'   height='50' />".format(self.image.url))


class Category(models.Model):
    parent = models.ForeignKey('Category', on_delete=models.CASCADE, null=True, blank=True, default=None)
    title = models.CharField(max_length=150, null=False, blank=False)
    slug = models.CharField(max_length=150, unique=True, null=False, blank=False)
    keywords = models.CharField(max_length=150, null=False, blank=False)
    description = models.CharField(max_length=150, null=False, blank=False)
    image = models.ImageField(upload_to='images/')
    status = models.BooleanField(default=False, choices=job_status, null=False, blank=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    @property
    def subcategories(self):
        return Category.objects.filter(parent=self)

    @property
    def jobs(self):
        if self.parent is None:
            return []
        else:
            return Job.objects.filter(category=self)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name_plural = 'Categories'


comment_status = (
    ('Published', 'Published'),
    ('Unpublished', 'Unpublished'),
)


class Comment(models.Model):
    comment = models.TextField(blank=False, null=False, )
    job = models.ForeignKey('Job', on_delete=models.CASCADE, blank=False, null=False, )
    user = models.ForeignKey(Customer, on_delete=models.CASCADE, blank=False, null=False, )
    ip = models.GenericIPAddressField(null=False, blank=False)
    status = models.CharField(max_length=15, choices=comment_status, default='Published', null=False, blank=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    @property
    def short(self):
        if len(self.comment) > 10:
            return self.comment[0:9] + '...'
        else:
            return self.comment

    def __str__(self):
        return self.short


application_status = (
    ('Pending', 'Pending'),
    ('Accepted', 'Accepted'),
    ('Rejected', 'Rejected'),
)


class Application(models.Model):
    job = models.ForeignKey('Job', on_delete=models.CASCADE, blank=False, null=False)
    applicant = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False)
    status = models.CharField(max_length=15, choices=application_status, blank=False, null=False, default='Pending')
    ip = models.GenericIPAddressField(null=False, blank=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.id} - {self.job.title}'

    class Meta:
        unique_together = ['job', 'applicant']


class Saved(models.Model):
    job = models.ForeignKey('Job', on_delete=models.CASCADE, blank=False, null=False)
    applicant = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False)
    ip = models.GenericIPAddressField(null=False, blank=False)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.id} - {self.job.title}'

    class Meta:
        verbose_name_plural = 'Saved(s)'
        unique_together = ['job', 'applicant']





# class JobComment(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False)
#     job = models.ForeignKey('Job', on_delete=models.CASCADE, blank=False, null=False)
#     comment = models.TextField(blank=False, null=False)
#     ip = models.GenericIPAddressField(null=False, blank=False, default='127.0.0.1')
#     status = models.CharField(max_length=15, choices=comment_status, default='Published', null=False, blank=False)
#     created_at = models.DateTimeField(default=timezone.now)
#     updated_at = models.DateTimeField(default=timezone.now)
#



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
