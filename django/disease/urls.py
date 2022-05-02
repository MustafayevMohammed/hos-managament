from django.urls import path
from . import views

app_name = "disease"

urlpatterns = [
    path("panel/<str:id>",views.OperationPanelView.as_view(),name = "panel"),
    path("list/",views.OperationListView.as_view(),name = "list"),
    path("create_operation/",views.OperationCreateView.as_view(),name = "create"),
    path("active-deactivate-opration/<str:id>",views.ActivateDeactivateOperation.as_view(),name = "activate_deactivate"),
    path("active-operations",views.ActiveOperationsListView.as_view(),name = "active_operations"),
]
