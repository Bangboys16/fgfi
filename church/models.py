from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.utils.text import slugify


# Model for church services (Sunday, Weekday, etc.)

class Service(models.Model):
    SERVICE_TYPE_CHOICES = [
        ('Sunday', 'Sunday Service'),
        ('Weekday', 'Weekday Service'),
        ('Special', 'Special Service')
    ]

    service_type = models.CharField(max_length=10, choices=SERVICE_TYPE_CHOICES)
    title = models.CharField(max_length=200)
    #date = models.DateField()
    day = models.CharField(default="Add day of service", max_length=20)
    time = models.TimeField()
    description = models.TextField()
    location = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.title} ({self.service_type})"
    
class Announcement(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    date_posted = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title
    

class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.CharField(max_length=100)
    date_posted = models.DateField(auto_now_add=True)
    poster = models.ImageField(upload_to='images/', blank=True, null=True)
    category = models.CharField(max_length=100)
    slug = models.SlugField(max_length=200, unique=True, blank=True)

    def save(self, *args, **kwargs):
        # Automatically generate slug from title if it's not set
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
    

class Donation(models.Model):
    bank_name = models.CharField(max_length=100, default="Uba", help_text="Enter the church's bank name")
    account_name = models.CharField(max_length=100, default="freegraceinternational", help_text="Enter the church's account name")
    bank_account = models.CharField(max_length=100, help_text="Enter the church's bank account details")

    def __str__(self):
        return self.bank_name

class Branch(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    location = models.CharField(max_length=100)
    phone_number = models.CharField (max_length=30)
    email = models.EmailField()
    service_times = models.TextField()
    latitude = models.DecimalField(max_digits=9, decimal_places=7)
    longitude = models.DecimalField(max_digits=9, decimal_places=7)

    def __str__(self):
        return self.name
    
# Create your models here.
class Daily_Devotional(models.Model):
    bible_portion = models.CharField(max_length=255)
    text = models.TextField()  
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.bible_portion  

class Sermon(models.Model):
    title = models.CharField(max_length=200)
    preacher = models.CharField(max_length=100)
    date_preached = models.DateField()
    description = models.TextField()
    pdf_file = models.FileField(upload_to='pdfs/', null=True, blank=True)
    audio_file = models.FileField(upload_to='audio/', null=True, blank=True)
    video_file = models.FileField(upload_to='videos/', null=True, blank=True)
    posted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    poster = models.ImageField(upload_to='images/', blank=True, null=True)

    def save(self, *args, **kwargs):
        # Automatically generate slug from title if it's not set
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Sermons'

    def __str__(self):
        return self.title

class GeneralOverseerMessage(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    video_message = models.FileField(upload_to='videos/')
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title