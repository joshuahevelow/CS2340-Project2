from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import JobSeeker, User

class Signup(UserCreationForm):
    job = forms.ChoiceField(choices= User.ROLE_CHOICES)
    class Meta:
        model = User
        fields = ["username", "role", "password1", "password2"]

class JobSeek(forms.ModelForm):
    class Meta:
        model = JobSeeker
        fields = ["headline", "skills", "education", "experience","links"
                  ]
class JobSeekForm(forms.Form):
    title = forms.ChoiceField(required=False)
    skills = forms.ChoiceField(required=False)
    location = forms.ChoiceField(required=False)
    salary = forms.ChoiceField(required=False)
    is_remote = forms.ChoiceField(required=False, choices=[("", ""), ("remote", "remote"), ("on-site", "on-site")])
    is_visa = forms.ChoiceField(required= False, choices=[("", ""), ("may offer sponsorship","may offer sponsorship"), ("does not offer sponsorship", "does not offer sponsorship")])
    min_salary = forms.IntegerField(required=False)
    max_salary = forms.IntegerField(required=False)