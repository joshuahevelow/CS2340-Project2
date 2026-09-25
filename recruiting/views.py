from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseForbidden
from .forms import  JobSeekForm, JobSeek, Signup
from .models import Job, JobSeeker, Recruiter
# Create your views here.

def signup(request):
    form = Signup(request.POST)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        if user.role == "seeker":
            JobSeeker.objects.create(user = user)
        else:
            Recruiter.objects.create(user=user)
        login(request, user)
        return redirect("jobs")
    return render(request, "recruiting/form.html", {"title": "Sign Up", "form": form,})
@login_required
def edit(request):
    if request.user.role != "seeker":
        return HttpResponseForbidden("Only job seekers")
    seeker, made_file = JobSeek.objects.get_or_create(user=request)
    form = JobSeek(request.POST)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("view_profile", seeker_id = seeker.id)
    return render(request, "recruiting/form.html", {"title": "Edit profile", "form": form, })

def view(request, seeker_id):
    seeker = get_object_or_404(JobSeeker, id = seeker_id)
    return render(request, "recruiting/profile.html", {"seeker" : seeker})

def job_search(request):
    open_job = Job.objects.filter(is_open =True)
    form = JobSeekForm(request.GET)
    if form.is_valid():
        if form.cleaned_data["title"]:
            open_job = open_job.filter(title=form.cleaned_data["title"])
    if form.is_valid():
        if form.cleaned_data["skills"]:
            open_job = open_job.filter(skills=form.cleaned_data["skills"])
    if form.is_valid():
        if form.cleaned_data["location"]:
            open_job = open_job.filter(location=form.cleaned_data["location"])
    if form.is_valid():
        if form.cleaned_data["min_salary"] is not None:
            open_job = open_job.filter(min_salary__gte=form.cleaned_data["min_salary"])
    if form.is_valid():
        if form.cleaned_data["max_salary"] is not None:
            open_job = open_job.filter(max_salary__lte=form.cleaned_data["max_salary"])
    if form.is_valid():
        if form.cleaned_data["is_remote"] == "remote":
            open_job = open_job.filter(remote=True)
    if form.is_valid():
        if form.cleaned_data["is_remote"] == "onsite":
            open_job = open_job.filter(remote=False)
    if form.is_valid():
        if form.cleaned_data["is_visa"] == "yes sponsorship":
            open_job = open_job.filter(visa_sponsorship= True)
    if form.is_valid():
        if form.cleaned_data["is_visa"] == "does not offer sponsorship":
            open_job = open_job.filter(visa_sponsorship=False)
    return  render(request, "recruiting/job_search.html", {"jobs": open_job, "form": form})