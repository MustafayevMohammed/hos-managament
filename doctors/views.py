from urllib import request
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import View, UpdateView
from doctors.models import DoctorField, DoctorModel
from disease.models import OperationModel
from account.models import BloodTypeModel, CustomUserModel, GenderModel
from django.contrib.auth.mixins import LoginRequiredMixin
from patients.models import PatientModel, PeopleWithPatientModel
from django.views.generic import FormView, CreateView
from doctors.forms import DoctorForm
from account.forms import RegisterForm
from django.contrib.auth import login

# Create your views here.

class DoctorPanelView(LoginRequiredMixin,View):
    login_url = reverse_lazy("doctor:login")
    
    def get(self,request,id):
        doctor = DoctorModel.objects.get(id=id)

        active_patients = PeopleWithPatientModel.objects.filter(doctor = doctor, is_active = True)
        deactive_patients = PeopleWithPatientModel.objects.filter(doctor = doctor, is_active = False)

        last_five_ppl_with_pat = PeopleWithPatientModel.objects.filter(doctor = doctor).order_by("-id")[:5][::-1]
        last_five_operation = OperationModel.objects.filter(doctor = doctor).order_by("-id")[:5][::-1]
        
        if request.user != doctor.user:
            if DoctorModel.objects.filter(user = request.user).first():
                return redirect("doctor:panel",request.user.user_doctors.id)
        elif request.user.is_staff:
            return redirect("doctor:panel",doctor.id)

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
            return redirect("doctor:panel",request.user.user_doctors.id)
        
        context = {
            "doctors":doctors,
            "active_doctors":active_doctors,
            "deactive_doctors":deactive_doctors,
        }
        return render(request,"doctors.html",context)


class PatientsOfDoctorView(LoginRequiredMixin,View):
    login_url = reverse_lazy("doctor:login")

    def get(self,request,id):
        doctor = DoctorModel.objects.get(id=id)

        patients = PeopleWithPatientModel.objects.filter(doctor = doctor)
        active_patients = PeopleWithPatientModel.objects.filter(doctor = doctor,is_active = True)
        deactive_patients = PeopleWithPatientModel.objects.filter(doctor = doctor,is_active = False)

        if request.user != doctor.user:
            if DoctorModel.objects.filter(user = request.user).first():
                return redirect("doctor:panel",request.user.user_doctors.id)
        elif request.user.is_staff:
            return redirect("doctor:patients",doctor.id)

        context = {
            "patients":patients,
            "active_patients":active_patients,
            "deactive_patients":deactive_patients,
            "doctor":doctor
        }
        
        return render(request,"patients_of_doctor.html",context)


class OperatationsOfDoctorView(LoginRequiredMixin,View):
    login_url = reverse_lazy("doctor:login")

    def get(self,request,id):
        doctor = DoctorModel.objects.get(id=id)

        operations = OperationModel.objects.filter(doctor = doctor)
        active_operations = OperationModel.objects.filter(doctor = doctor,is_active = True)
        deactive_operations = OperationModel.objects.filter(doctor = doctor,is_active = False)

        if request.user != doctor.user:
            if DoctorModel.objects.filter(user = request.user).first():
                return redirect("doctor:panel",request.user.user_doctors.id)
        elif request.user.is_staff:
            return redirect("doctor:operations",doctor.id)

        context = {
            "operations":operations,
            "active_operations":active_operations,
            "deactive_operations":deactive_operations,
            "doctor":doctor
        }
        return render(request,"operations_of_doctor.html",context)




class DoctorEditView(UpdateView):
    template_name = "doctor_edit.html"
    form_class = DoctorForm

    def get_object(self,*args, **kwargs):
        return DoctorModel.objects.get(id=self.kwargs.get("id"))

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context["doctor"] = self.get_object
        context["gender_choices"] = GenderModel.objects.all()
        context["working_field_choices"] = DoctorField.objects.all()
        context["blood_type_choices"] = BloodTypeModel.objects.all()
        return context
    
    def dispatch(self, request, *args, **kwargs):
        doctor = DoctorModel.objects.get(id=self.kwargs.get("id"))
        
        if doctor.user != request.user:
            if DoctorModel.objects.filter(user = request.user).first():
                return redirect("/")
        elif request.user.is_staff:
            return redirect("doctor:edit",doctor.id)
            
        return super().dispatch(request, *args, **kwargs)

    
    

def admin_permission_waiting(request):
    if request.user.is_accepted == True:
        return redirect("doctor:admin_permission_accepted")

    return render(request,"admin_permission_waiting.html")

def admin_permission_accepted(request):
    if request.user.is_accepted == False:
        return redirect("doctor:admin_permission_waiting")

    return render(request,"admin_permission_accepted.html")


class DoctorUserRegister(CreateView):
    template_name = 'doctor_user_register.html'
    success_url = reverse_lazy('doctor:admin_permission_waiting')
    form_class = RegisterForm
    
    def form_valid(self,form,*args, **kwargs):
        user = form.save()
        login(self.request,user)
        return redirect("doctor:admin_permission_waiting")


class DoctorCreateView(CreateView):
    template_name = "doctor_create.html"
    form_class = DoctorForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["working_field_choices"] = DoctorField.objects.all()
        context["gender_choices"] = GenderModel.objects.all()
        context["blood_type_choices"] = BloodTypeModel.objects.all()
        return context
    
    def form_valid(self,form,*args, **kwargs):
        instance = form.save(commit=False)
        instance.user = self.request.user
        instance.save()
        return redirect("/")
    
    def form_invalid(self,form,*args, **kwargs):
        print(form.errors)
        return super().form_invalid(form)

        




def doctor_logs(request):
    return render(request,"doctor_logs.html")



def doctor_login(request):
    return render(request,"doctor_login.html")




# def admin_register(request):
#     return render(request,"admin_register.html")

# def admin_login(request):
#     return render(request,"admin_login.html")





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