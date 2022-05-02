from django.urls import path
from todo import views 

app_name = 'todo'


urlpatterns = [
    path("complete/<str:id>",views.completeTask ,name="complete")
]
