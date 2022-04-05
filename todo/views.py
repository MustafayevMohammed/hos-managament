from django.http import HttpResponse
from django.shortcuts import redirect, render
from todo.models import *
from django.utils import timezone
from todo.forms import TaskForm
from doctors.models import DoctorModel
from django.contrib.auth.decorators import login_required
from account.models import CustomUserModel
# Create your views here.


@login_required(login_url="doctor:login")
def completeTask(request,id):
    task = TaskModel.objects.filter(id=id).first()
    
    user_with_no_doctors = CustomUserModel.objects.filter(id=request.user.id,user_doctors = None,is_staff = False).first()

    if request.user == task.user:
        task.is_active = False
        task.save()
        return redirect("/#todo")
    else:
        if request.user.is_staff == False:
            if user_with_no_doctors:
                return redirect("doctor:create")
            return redirect("doctor:panel",request.user.user_doctors.id)
        
