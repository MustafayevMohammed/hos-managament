from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import View
from doctors.models import DoctorModel
from disease.models import OperationModel
from account.models import CustomUserModel
from django.contrib.auth.mixins import LoginRequiredMixin
from patients.models import PatientModel, PeopleWithPatientModel
from django.views.generic import FormView

# Create your views here.

class DoctorPanelView(LoginRequiredMixin,View):
    login_url = reverse_lazy("doctor:login")
    
    def get(self,request,id):
        doctor_user = CustomUserModel.objects.filter(id=id).first()
        doctor = doctor_user.user_doctors

        active_patients = PeopleWithPatientModel.objects.filter(doctor = doctor, is_active = True)
        deactive_patients = PeopleWithPatientModel.objects.filter(doctor = doctor, is_active = False)

        last_five_ppl_with_pat = PeopleWithPatientModel.objects.filter(doctor = doctor).order_by("-id")[:5][::-1]
        last_five_operation = OperationModel.objects.filter(doctor = doctor).order_by("-id")[:5][::-1]
        
        if request.user != doctor_user:
            if DoctorModel.objects.filter(user = request.user).first():
                return redirect("doctor:panel",request.user.id)
        elif request.user.is_staff:
            return redirect("doctor:panel",doctor_user.id)

        context = {
            "doctor":doctor,
            "active_patients":active_patients,
            "deactive_patients":deactive_patients,
            "last_five_ppl_with_pat":last_five_ppl_with_pat,
            "last_five_operation":last_five_operation,
        }
        return render(request,"doctor_panel.html",context)
        

class DoctorListView(LoginRequiredMixin,View):
    login_url = reverse_lazy("doctor:login")

    def get(self,request):
        doctors = DoctorModel.objects.all()
        active_doctors = DoctorModel.objects.filter(is_active = True)
        deactive_doctors = DoctorModel.objects.filter(is_active = False)


        if request.user.is_staff == False:
            return redirect("doctor:panel",request.user.id)
        
        context = {
            "doctors":doctors,
            "active_doctors":active_doctors,
            "deactive_doctors":deactive_doctors,
        }
        return render(request,"doctors.html",context)


class PatientsOfDoctorView(LoginRequiredMixin,View):
    login_url = reverse_lazy("doctor:login")

    def get(self,request,id):
        doctor_user = CustomUserModel.objects.get(id=id)
        doctor = doctor_user.user_doctors

        patients = PeopleWithPatientModel.objects.filter(doctor = doctor)
        active_patients = PeopleWithPatientModel.objects.filter(doctor = doctor,is_active = True)
        deactive_patients = PeopleWithPatientModel.objects.filter(doctor = doctor,is_active = False)

        if request.user != doctor_user:
            if DoctorModel.objects.filter(user = request.user).first():
                return redirect("doctor:panel",request.user.id)
        elif request.user.is_staff:
            return redirect("doctor:patients",doctor_user.id)

        context = {
            "patients":patients,
            "active_patients":active_patients,
            "deactive_patients":deactive_patients,
            "doctor":doctor
        }
        
        return render(request,"patients_of_doctor.html",context)


class OperatationsOfDoctorView(View):

    def get(self,request,id):
        doctor_user = CustomUserModel.objects.get(id=id)
        doctor = doctor_user.user_doctors

        operations = OperationModel.objects.filter(doctor = doctor)
        active_operations = OperationModel.objects.filter(doctor = doctor,is_active = True)
        deactive_operations = OperationModel.objects.filter(doctor = doctor,is_active = False)


        if request.user != doctor_user:
            if DoctorModel.objects.filter(user = request.user).first():
                return redirect("doctor:panel",request.user.id)
        elif request.user.is_staff:
            return redirect("doctor:operations",doctor_user.id)


        context = {
            "operations":operations,
            "active_operations":active_operations,
            "deactive_operations":deactive_operations,
            "doctor":doctor
        }

        return render(request,"operations_of_doctor.html",context)




def doctor_edit(request):
    return render(request,"doctor_edit.html")

class DoctorEditFormView(FormView):
    template_name = "doctor_edit.html"


def doctor_logs(request):
    return render(request,"doctor_logs.html")

def doctor_user_register(request):
    return render(request,"doctor_user_register.html")

def doctor_register(request):
    return render(request,"doctor_register.html")

def doctor_login(request):
    return render(request,"doctor_login.html")




def admin_register(request):
    return render(request,"admin_register.html")

def admin_login(request):
    return render(request,"admin_login.html")

def admin_permission_waiting(request):
    return render(request,"admin_permission_waiting.html")

def admin_permission_accepted(request):
    return render(request,"admin_permission_accepted.html")




def charts(request):
    return render(request,"charts/chartjs.html")

def forms(request):
    return render(request,"forms/basic_elements.html")

def icons(request):
    return render(request,"icons/mdi.html")

def tables(request):
    return render(request,"tables/basic-table.html")

def ui_features(request):
    return render(request,"ui-features/buttons.html")

def ui_features2(request):
    return render(request,"ui-features/dropdowns.html")

def ui_features3(request):
    return render(request,"ui-features/typography.html")