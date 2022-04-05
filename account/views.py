from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from doctors.models import DoctorModel
from patients.models import PatientModel
from disease.models import OperationModel
from todo.models import *
from todo.forms import TaskForm
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from account.models import CustomUserModel
# Create your views here.


class AdminPanelView(LoginRequiredMixin,View):
    login_url = reverse_lazy("doctor:login")

    def get(self,request):
        user_with_no_doctors = CustomUserModel.objects.filter(id=request.user.id,user_doctors = None,is_staff = False).first()
        if request.user.is_staff == False:
            if user_with_no_doctors:
                return redirect("doctor:create")
            return redirect("doctor:panel",request.user.user_doctors.id)

        doctors = DoctorModel.objects.all()
        patients = PatientModel.objects.all()
        operations = OperationModel.objects.all()

        for operation in operations:
            pass

        last_five_patient = PatientModel.objects.all().order_by()[:5][::-1]
        last_five_operation = OperationModel.objects.all().order_by("-id")[:5][::-1]
        last_four_doctor = DoctorModel.objects.all().order_by("-id")[:5]
        
        tasks = TaskModel.objects.filter(user=request.user,is_active=True)

        context = {
            "doctors":doctors,
            "patients":patients,
            "operations":operations,
            "last_five_patient":last_five_patient,
            "last_five_operation":last_five_operation,
            "last_four_doctor":last_four_doctor,
            "tasks":tasks,
        }
        return render(request,"admin_panel.html",context)

    def post(self,request):
        form = TaskForm(request.POST)
        # print(" ")
        # print("------------------------")
        # print(" ")
        # print(form)
        # print(form.errors)
        
        if form.is_valid():
            # form.save()
            data = TaskModel()
            data.user = request.user
            data.name = form.cleaned_data["name"]
            data.is_active = True
            data.save()
        return redirect("/#todo")



def notifications(request):
    return render(request,"notifications.html")