from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from disease.models import OperationModel
from django.contrib.auth.mixins import LoginRequiredMixin
from doctors.models import DoctorModel
# Create your views here.

class OperationListView(LoginRequiredMixin,View):
    login_url = reverse_lazy("doctor:login")

    def get(self,request):
        operations = OperationModel.objects.all()
        active_operations = OperationModel.objects.filter(is_active = True)
        deactive_operations = OperationModel.objects.filter(is_active = False)

        if request.user.is_staff == False:
            return redirect("doctor:panel",request.user.id)

        context = {
            "operations":operations,
            "active_operations":active_operations,
            "deactive_operations":deactive_operations,
        }
        return render(request,"operations.html",context)



class OperationPanelView(LoginRequiredMixin,View):
    login_url = reverse_lazy("doctor:login")

    def get(self,request,id):
        operation = OperationModel.objects.get(id=id)
        doctor = DoctorModel.objects.filter(doctor_operations = operation, user = request.user).first()

        if not doctor:
            if DoctorModel.objects.filter(user = request.user):
                return redirect("doctor:panel",request.user.id)

        context = {
            "operation":operation,
        }
        return render(request,"operation_detail.html",context)

def create_operation(request):
    return render(request,"create_operation.html")