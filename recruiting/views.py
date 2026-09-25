from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseForbidden
from .forms import  JobSeekForm, JobSeek, Signup
from .models import Job, JobSeeker, Recruiter, Application

def signup(request):
    form = Signup(request.POST)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        if user.role == "seeker":
            JobSeeker.objects.create(user = user)
        else:
            Recruiter.objects.create(user=user)
        login(request, user)
        return redirect("job_search")
    return render(request, "recruiting/form.html", {"title": "Sign Up", "form": form,})

@login_required
def edit(request):
    if request.user.role != "seeker":
        return HttpResponseForbidden("Only job seekers")
    seeker, _ = JobSeek.objects.get_or_create(user=request.user)
    form = JobSeek(request.POST or None, instance=seeker)
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
            open_job = open_job.filter(title__icontains=form.cleaned_data["title"])
        if form.cleaned_data["skills"]:
            open_job = open_job.filter(skills__icontains=form.cleaned_data["skills"])
        if form.cleaned_data["location"]:
            open_job = open_job.filter(location__icontains=form.cleaned_data["location"])
        if form.cleaned_data["min_salary"] is not None:
            open_job = open_job.filter(min_salary__gte=form.cleaned_data["min_salary"])
        if form.cleaned_data["max_salary"] is not None:
            open_job = open_job.filter(max_salary__lte=form.cleaned_data["max_salary"])
        if form.cleaned_data["is_remote"] == "remote":
            open_job = open_job.filter(remote=True)
        if form.cleaned_data["is_remote"] == "onsite":
            open_job = open_job.filter(remote=False)
        if form.cleaned_data["is_visa"] == "yes we offer sponsorship":
            open_job = open_job.filter(visa_sponsorship= True)
        if form.cleaned_data["is_visa"] == "does not offer sponsorship":
            open_job = open_job.filter(visa_sponsorship=False)
    return render(request, "recruiting/job_search.html", {"jobs": open_job, "form": form})

@login_required
def apply_to_job(request, job_id):
    if request.user.role != "seeker":
        return HttpResponseForbidden("Only job seekers can apply")
    job = get_object_or_404(Job, id=job_id)
    seeker = get_object_or_404(JobSeeker, user=request.user)
    if request.method == "POST":
        Application.objects.get_or_create(
            job=job, seeker=seeker,
            defaults={"note": request.POST.get("note", "")}
        )
        return redirect("job_search")
    return HttpResponseForbidden("Use POST")

@login_required
def my_applications(request):
    seeker = get_object_or_404(JobSeeker, user=request.user)
    apps = Application.objects.filter(seeker=seeker).select_related("job").order_by("-applied_at")
    return render(request, "recruiting/applications.html", {"apps": apps})