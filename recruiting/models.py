from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser):
    ROLE_CHOICES = [
        ("seeker", "Job Seeker"), ("recruiter", "Recruiter"),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="seeker")
class JobSeeker(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    headline = models.CharField(max_length=150, blank=True)
    education = models.TextField(blank=True)
    skills = models.TextField(blank=True)
    experience = models.TextField(blank=True)
    links = models.TextField(blank=True)
    def __str__(self):
        return self.user.username

class Recruiter(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    company = models.CharField(max_length=150)
    def __str__(self):
        return self.user.username

class Job(models.Model):
    recruiter = models.ForeignKey(Recruiter, on_delete=models.CASCADE )
    title = models.CharField(max_length=150)
    skills = models.TextField(blank=True)
    location = models.CharField(max_length=150)
    salary = models.CharField(max_length=150, blank=True)
    min_salary = models.PositiveIntegerField(null=True, blank=True)
    max_salary = models.PositiveIntegerField(null=True, blank=True)
    remote = models.BooleanField(default=False)
    visa_sponsorship = models.BooleanField(default=False)
    is_open = models.BooleanField(default=True)

    def __str__(self):
        return self.title