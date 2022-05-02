from django import forms
from django.db.models import fields
from django.forms import widgets
from todo.models import *

class TaskForm(forms.ModelForm):
    
    class Meta:
        fields = ("name","is_active")
        model = TaskModel
        
