"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from . import views
app_name = 'doctor'

# path("admin_register/",views.admin_register),
# path("admin_login/",views.admin_login),


urlpatterns = [
    path("admin_permission_waiting/",views.admin_permission_waiting,name = "admin_permission_waiting"),
    path("admin_permission_accepted/",views.admin_permission_accepted,name = "admin_permission_accepted"),
    

    path("panel/<int:id>",views.DoctorPanelView.as_view(),name = "panel"),
    path("list/",views.DoctorListView.as_view(),name = "list"),
    path("edit/<str:id>",views.DoctorEditView.as_view(),name = "edit"),
    path("logs/",views.doctor_logs,name = "logs"),
    path("register/",views.DoctorUserRegister.as_view(), name = "register"),
    path("create/",views.DoctorCreateView.as_view(), name = "create"),
    path("login/",views.doctor_login, name = "login"),
    
    path("patients/<str:id>",views.PatientsOfDoctorView.as_view(),name="patients"),
    path("operations/<str:id>",views.OperatationsOfDoctorView.as_view(),name="operations"),

    # path("charts/",views.charts),
    # path("forms",views.forms),
    # path("icons",views.icons),
    # path("tables",views.tables),
    path("ui_features",views.ui_features),
    path("ui_features2",views.ui_features2),
    path("ui_features3",views.ui_features3),
]
