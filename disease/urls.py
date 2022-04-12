from django.urls import path
from . import views

app_name = "disease"

urlpatterns = [
    path("panel/<str:id>",views.OperationPanelView.as_view(),name = "panel"),
    path("list/",views.OperationListView.as_view(),name = "list"),
    path("create_operation/",views.OperationCreateView.as_view(),name = "create"),
]
