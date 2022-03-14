from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from disease.models import DiseaseModel, OperationModel
from patients.forms import CreatePatientForm
from patients.models import PatientModel, PeopleWithPatientModel, BloodTypeModel, GenderModel
from doctors.models import DoctorModel
from django.contrib.auth.mixins import LoginRequiredMixin
import phonenumbers
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
        gender_choices = GenderModel.objects.all()
        blood_type_choices = BloodTypeModel.objects.all()
        diseases = DiseaseModel.objects.all()

        errors = self.form.errors

        context = {
            "gender_choices":gender_choices,
            "blood_type_choices":blood_type_choices,
            "diseases":diseases,
            # "errors": errors,
        }
        return render(request,"create_patient.html",context)


    def post(self, request):
        form = CreatePatientForm(request.POST)
        print(form.errors)
    
        if form.is_valid():

            first_name = form.cleaned_data.get("first_name")
            last_name = form.cleaned_data.get("last_name")
            phonenumber = form.cleaned_data.get("phonenumber")
            gender = form.cleaned_data.get("gender")
            blood_type = form.cleaned_data.get("blood_type")
            born_date = form.cleaned_data.get("born_date")
            expected_discharging_date = form.cleaned_data.get("expected_discharging_date")
            diseases = form.cleaned_data.get("disease")
            additional_information = form.cleaned_data.get("additional_information")

            patient_diseases = DiseaseModel.objects.filter(id__in = diseases)

            try:
                instance = PatientModel.objects.create(first_name = first_name, last_name = last_name, gender = gender, blood_type = blood_type, born_date = born_date, expected_discharging_date = expected_discharging_date, additional_information = additional_information, is_active = True)
            except:
                return self.form_invalid(self, form)
            instance.disease.add(*patient_diseases)

            try:
                phonenum = phonenumbers.parse(phonenumber)
            except phonenumbers.phonenumberutil.NumberParseException:
                raise ValueError("sehv")
            
            else:
                instance.phonenumber = phonenum

            return redirect("/")
        
        return render(request, "create_patient.html", {'form': form})
    

    def form_invalid(self, request, form, *args, **kwargs):
        errors = form.errors
        # context = {
        #     "errors":errors
        # }
        return render(request, "create_patient.html", {'errors': form.errors})





def add_patient_status(request,id):
    return render(request,"add_patient_status.html")

def patient_edit(request,id):
    return render(request,"patient_edit.html")

def ppl_with_patient(request,id):
    return render(request,"add_ppl_with_patient.html")


def patient_logs(request):
    return render(request,"patient_logs.html")
