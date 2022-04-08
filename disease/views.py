from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from account.models import CustomUserModel
from disease.models import OperationModel
from django.contrib.auth.mixins import LoginRequiredMixin
from doctors.models import DoctorModel
# Create your views here.

class OperationListView(LoginRequiredMixin,View):
    login_url = reverse_lazy("doctor:login")

    def get(self,request):
        user_with_no_doctors = CustomUserModel.objects.filter(id=request.user.id,user_doctors = None,is_staff = False,is_accepted = True).first()

        operations = OperationModel.objects.all()
        active_operations = OperationModel.objects.filter(is_active = True)
        deactive_operations = OperationModel.objects.filter(is_active = False)

        if request.user.is_staff == False:
            if user_with_no_doctors:
                return redirect("doctor:create")

            elif request.user.is_accepted == False:
                return redirect("doctor:admin_permission_waiting")

            return redirect("doctor:panel",request.user.user_doctors.id)

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
        # request_doctor = DoctorModel.objects.filter(user = request.user,user__is_staff=False).first()
        user_with_no_doctors = CustomUserModel.objects.filter(id=request.user.id,user_doctors = None,is_staff = False,is_accepted = True).first()
        # print(doctor)

        if not doctor:
            if DoctorModel.objects.filter(user = request.user, user__is_accepted = True).exists():
                return redirect("doctor:panel",request.user.user_doctors.id)

            elif DoctorModel.objects.filter(user = request.user, user__is_accepted = False).exists():
                return redirect("doctor:admin_permission_waiting")

            elif user_with_no_doctors:
                return redirect("doctor:create")
                
            elif request.user.is_accepted == False:
                return redirect("doctor:admin_permission_waiting")
                
        elif doctor.user.is_accepted == False:
            return redirect("doctor:admin_permission_waiting")

        context = {
            "operation":operation,
        }
        return render(request,"operation_detail.html",context)

def create_operation(request):
    return render(request,"create_operation.html")