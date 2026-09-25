from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Job, User, JobSeeker, Recruiter
# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(JobSeeker)
admin.site.register(Job)
admin.site.register(Recruiter)