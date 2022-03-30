from . import views
from django.urls import path

app_name  = "patient"

urlpatterns = [
    path("create/",views.PatientCreateView.as_view(), name = "create"),
    path("list/",views.PatientListView.as_view() ,name = "list"),
    path("panel/<str:id>",views.PatientPanelView.as_view(), name = "panel"),
    path("edit/<str:id>",views.PatientEditView.as_view(), name = "edit"),
    path("add_status/<str:id>",views.AddPatientStatusView.as_view(),name = "add_status"),
    path("add_ppl_with_patient/<str:id>",views.AddPplWithPatientView.as_view(),name = "add_ppl_with_patient"),
    path("list_ppl_with_patient/<str:id>",views.ListPplWithPatientView.as_view(),name = "list_ppl_with_patient"),
    path("logs/<str:id>",views.PatientLogsView.as_view(),name = "logs"),
    path("activate-deactivate-patient/<str:id>",views.ActivateDeactivatePatientView.as_view(),name = "activate_deactivate"),
]
