from . import views
from django.urls import path

app_name  = "patient"

urlpatterns = [
    path("create/",views.PatientCreateView.as_view(), name = "create"),
    path("list/",views.PatientListView.as_view() ,name = "list"),
    path("panel/<str:id>",views.PatientPanelView.as_view(), name = "panel"),
    path("edit/<str:id>",views.patient_edit, name = "edit"),
    path("add_status/<str:id>",views.add_patient_status,name = "add_status"),
    path("add_ppl_with_patient/<str:id>",views.ppl_with_patient,name = "add_ppl_with_patient"),
    path("logs/",views.patient_logs,name = "logs"),
]
