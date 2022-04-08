from django.urls import path
from . import views

app_name = 'account'


urlpatterns = [
    path("",views.AdminPanelView.as_view(),name="admin_panel"),
    path("notifications/",views.NotificationsView.as_view(),name="notifications"),
]
