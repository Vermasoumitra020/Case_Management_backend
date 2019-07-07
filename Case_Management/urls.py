"""Case_Management URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path, include
from manager_login import views
from manager_app.views import TaskViews, ViewTaskView, UpdateTaskView, DeleteTaskView
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('manager-registration/', views.ManagerSignupView.as_view()),
    path('manage-login/', views.ManagerLoginView.as_view()),
    path('create-task/', TaskViews.as_view()),
    path('logout/', views.ManagerLogoutView.as_view()),
    path('view-tasks/', ViewTaskView.as_view()),
    path('delete/(?P<factory_id>[0-9a-f-]+)', DeleteTaskView.as_view()),
    path('update/', UpdateTaskView.as_view())
]
