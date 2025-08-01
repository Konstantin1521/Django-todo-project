"""
URL configuration for todo_manager project.

The `urlpatterns` list routes URLs to views_dir. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views_dir
    1. Add an import:  from my_app import views_dir
    2. Add a URL to urlpatterns:  path('', views_dir.home, name='home')
Class-based views_dir
    1. Add an import:  from other_app.views_dir import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views

from todo_list import views

from debug_toolbar.toolbar import debug_toolbar_urls


urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='todo_list/registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('', TemplateView.as_view(template_name="index.html"), name="index"),
    path('todos/', include("todo_list.urls")),
    path('admin/', admin.site.urls),
]

urlpatterns.extend(debug_toolbar_urls())