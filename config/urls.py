"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from recruiting import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("signup/", views.signup, name="signup"),
    path("login/", auth_views.LoginView.as_view(template_name="recruiting/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page="job_search"), name="logout"),
    path("profile/edit/", views.edit, name="edit_profile"),
    path("seekers/<int:seekers_id>", views.view, name="view_profile"),
    path("", views.job_search, name="job_search"),
    path("jobs/<int:id>/apply/", views.apply_to_job, name="apply_to_job"),
    path("applications/", views.my_applications, name="my_applications"),
]
