from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from disease.models import DiseaseModel, OperationModel
from patients.forms import CreatePatientForm
from patients.models import PatientModel, PeopleWithPatientModel
from doctors.models import DoctorModel
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.

class PatientListView(LoginRequiredMixin,View):
    login_url = reverse_lazy("doctor:login")
    
    def get(self,request):
        patients = PatientModel.objects.all()
        active_patients = PatientModel.objects.filter(is_active = True)
        deactive_patients = PatientModel.objects.filter(is_active = False)

        if request.user.is_staff == False:
            # if request.user
            return redirect("doctor:panel",request.user.id)

        context = {
            "patients":patients,
            "active_patients":active_patients,
            "deactive_patients":deactive_patients,
        }
        return render(request,"patients.html",context)


class PatientPanelView(LoginRequiredMixin,View):
    login_url = reverse_lazy("doctor:login")

    def get(self,request,id):
        patient = PatientModel.objects.get(id=id)
        ppl_with_patient = PeopleWithPatientModel.objects.filter(patient = patient)
        operations = OperationModel.objects.filter(patient = patient)
        doctor = DoctorModel.objects.filter(doctor_ppl_with_patient__in =  ppl_with_patient, user = request.user).first()

        if not doctor:
            if DoctorModel.objects.filter(user = request.user):
                return redirect("doctor:panel",request.user.id)

        context = {
            "patient":patient,
            "ppl_with_patient":ppl_with_patient,
            "operations":operations,
        }
        return render(request,"patient_panel.html",context)

class PatientCreateView(View):
    form = CreatePatientForm

    def get(self, request):
        gender_choices = PatientModel.GENDER_CHOICES
        blood_type_choices = PatientModel.BLOOD_TYPE_CHOICES
        diseases = DiseaseModel.objects.all()
        for gender in gender_choices:
            print(gender)
        context = {
            "gender_choices":gender_choices,
            "blood_type_choices":blood_type_choices,
            "diseases":diseases,
        }
        return render(request,"create_patient.html",context)

    def post(self, request):
        pass



def add_patient_status(request,id):
    return render(request,"add_patient_status.html")

def patient_edit(request,id):
    return render(request,"patient_edit.html")

def ppl_with_patient(request,id):
    return render(request,"add_ppl_with_patient.html")


def patient_logs(request):
    return render(request,"patient_logs.html")
