from ast import ExtSlice
from enum import Flag
from urllib import request
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy, reverse
from django.views import View
from disease.models import DiseaseModel, OperationModel
from patients.forms import AddPatientStatusForm, AddPeopleWithPatientForm, CreatePatientForm
from patients.models import PatientModel, PatientStatusModel, PeopleWithPatientModel, BloodTypeModel, GenderModel, StatusChoicesModel
from doctors.models import DoctorModel
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, UpdateView, FormView, ListView
import phonenumbers
from django.contrib import messages
from django.db.models import Q
from account.models import CustomUserModel
# Create your views here.

class PatientListView(LoginRequiredMixin,View):
    login_url = reverse_lazy("doctor:login")
    
    def get(self,request):
        user_with_no_doctors = CustomUserModel.objects.filter(id=request.user.id,user_doctors = None,is_staff = False,is_accepted = True).first()

        patients = PatientModel.objects.all()
        active_patients = PatientModel.objects.filter(is_active = True)
        deactive_patients = PatientModel.objects.filter(is_active = False)

        if request.user.is_staff == False:
            if user_with_no_doctors:
                return redirect("doctor:create")

            elif request.user.is_accepted == False:
                return redirect("doctor:admin_permission_waiting")

            return redirect("doctor:panel",request.user.user_doctors.id)

        context = {
            "patients":patients,
            "active_patients":active_patients,
            "deactive_patients":deactive_patients,
        }
        return render(request,"patients.html",context)


class PatientPanelView(LoginRequiredMixin,View):
    login_url = reverse_lazy("doctor:login")

    def get(self,request,id):
        user_with_no_doctors = CustomUserModel.objects.filter(id=request.user.id,user_doctors = None,is_staff = False,is_accepted = True).first()

        patient = PatientModel.objects.get(id=id)
        ppl_with_patient = PeopleWithPatientModel.objects.filter(patient = patient,is_active = True)
        operations = OperationModel.objects.filter(patient = patient)
        doctor = DoctorModel.objects.filter(doctor_ppl_with_patient__in = ppl_with_patient, user = request.user).first()

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
            "patient":patient,
            "ppl_with_patient":ppl_with_patient,
            "operations":operations,
        }
        return render(request,"patient_panel.html",context)



class PatientCreateView(LoginRequiredMixin,CreateView):
    template_name = "create_patient.html"
    form_class = CreatePatientForm
    login_url = reverse_lazy("doctor:login")


    def get_context_data(self,*args, **kwargs):
        context = super(PatientCreateView, self).get_context_data(*args,**kwargs)
        context["gender_choices"] = GenderModel.objects.all()
        context["blood_type_choices"] = BloodTypeModel.objects.all()
        context["diseases"] = DiseaseModel.objects.all()
        return context


    def form_valid(self,form, *args, **kwargs):
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
            phonenum = phonenumbers.parse(phonenumber)
        except:
            return super().form_invalid(form)
        else:
            instance = PatientModel.objects.create(first_name = first_name, last_name = last_name, gender = gender, blood_type = blood_type, born_date = born_date, expected_discharging_date = expected_discharging_date, additional_information = additional_information,phonenumber=phonenumber ,is_active = True)

        instance.disease.add(*patient_diseases)

        return redirect("patient:panel",instance.id)


    def form_invalid(self, form, *args, **kwargs):
        return super().form_invalid(form)
        # return render(request, "create_patient.html", {'form': form})   
    
    def dispatch(self,request,*args, **kwargs):
        user_with_no_doctors = CustomUserModel.objects.filter(id=request.user.id,user_doctors = None,is_staff = False,is_accepted = True).first()
        if request.user.is_staff == False:
            if user_with_no_doctors:
                return redirect("doctor:create")

            elif request.user.is_accepted == False:
                return redirect("doctor:admin_permission_waiting")

            return redirect("doctor:panel",request.user.user_doctors.id)
        return super().dispatch(request,*args, **kwargs)


class PatientEditView(LoginRequiredMixin,UpdateView):
    template_name = "patient_edit.html"
    form_class = CreatePatientForm
    login_url = reverse_lazy("doctor:login")

    # permission_required = "patientmodel.change_patientmodel"
    

    def get_object(self):
        return PatientModel.objects.get(id = self.kwargs.get("id"))


    def get_context_data(self,*args, **kwargs):
        context = super(PatientEditView, self).get_context_data(*args,**kwargs)
        context["gender_choices"] = GenderModel.objects.all()
        context["blood_type_choices"] = BloodTypeModel.objects.all()
        context["patient"] = self.get_object
        patient = PatientModel.objects.get(id = self.kwargs.get("id"))
        context["patient_diseases"] = patient.disease.all
        context["diseases"] = DiseaseModel.objects.exclude(id__in = patient.disease.values_list('id', flat=True))
        
        return context
    

    def dispatch(self,request,*args, **kwargs):

        user_with_no_doctors = CustomUserModel.objects.filter(id=request.user.id,user_doctors = None,is_staff = False,is_accepted = True).first()
        if request.user.is_staff == False:
            if user_with_no_doctors:
                return redirect("doctor:create")

            elif request.user.is_accepted == False:
                return redirect("doctor:admin_permission_waiting")

            return redirect("doctor:panel",request.user.user_doctors.id)
        return super().dispatch(request,*args, **kwargs)
    

    # def form_valid(self, form, *args, **kwargs):
    #     print(self.get_object)
    #     first_name = form.cleaned_data.get("first_name")
    #     last_name = form.cleaned_data.get("last_name")
    #     phonenumber = form.cleaned_data.get("phonenumber")
    #     gender = form.cleaned_data.get("gender")
    #     discharged_date = form.cleaned_data.get("discharged_date")
    #     born_date = form.cleaned_data.get("born_date")
    #     blood_type = form.cleaned_data.get("blood_type")
    #     diseases = form.cleaned_data.get("disease")
    #     joining_date = form.cleaned_data.get("joining_date")
    #     expected_discharging_date = form.cleaned_data.get("expected_discharging_date")
    #     additional_information = form.cleaned_data.get("additional_information")

    #     patient_diseases = DiseaseModel.objects.filter(name__in = diseases)
    #     print(patient_diseases)
    #     try:
    #         phonenum = phonenumbers.parse(phonenumber)
    #     except:
    #         return super().form_invalid(form)
    #     else:
    #         instance = PatientModel.objects.create(first_name = first_name, last_name = last_name, gender = gender, blood_type = blood_type, born_date = born_date, expected_discharging_date = expected_discharging_date, additional_information = additional_information,phonenumber = phonenumber,discharged_date = discharged_date, joining_date = joining_date, is_active = True)
        
    #     instance.disease.add(*patient_diseases)
    #     return redirect("patient:panel",instance.id)
    
    
    # def form_invalid(self,form, *args, **kwargs):
    #     return super().form_invalid(form)

    

class AddPatientStatusView(LoginRequiredMixin,CreateView):
    template_name = "add_patient_status.html"
    form_class = AddPatientStatusForm
    login_url = reverse_lazy("doctor:login")


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["patient_status"] = StatusChoicesModel.objects.all()
        return context


    def form_valid(self,form):
        status = form.cleaned_data.get("status")
        note = form.cleaned_data.get("note")

        doctor = DoctorModel.objects.get(user = self.request.user)
        patient = PatientModel.objects.get(id = self.kwargs.get("id"))

        PatientStatusModel.objects.create(status = status, note = note, doctor = doctor, patient = patient)
        
        return redirect("patient:panel",patient.id)
    

    def form_invalid(self,form,*args, **kwargs):
        return super().form_invalid(form)
    

    def dispatch(self, request, *args, **kwargs):
        patient = PatientModel.objects.get(id = kwargs.get("id"))
        doctor = DoctorModel.objects.filter(user = request.user).first()
        doctor_ppl_with_patient = PeopleWithPatientModel.objects.filter(patient = patient, doctor = doctor).first()

        user_with_no_doctors = CustomUserModel.objects.filter(id=request.user.id,user_doctors = None,is_staff = False,is_accepted = True).first()

        if doctor_ppl_with_patient is None:
            return redirect("/")

        elif user_with_no_doctors:
            return redirect("doctor:create")

        return super().dispatch(request, *args, **kwargs)
    


# class AddPplWithPatientView(View):
    
#     def get(self,request,*args, **kwargs):
#         patient = PatientModel.objects.get(id = kwargs.get("id"))
#         print(patient)
#         doctors_with_patient = PeopleWithPatientModel.objects.filter(patient = patient,is_active = True)
#         doctors = DoctorModel.objects.filter(~Q(doctor_ppl_with_patient__in = doctors_with_patient))

#         context = {
#             "doctors":doctors,
#             "doctors_with_patient":doctors_with_patient,
#             "patient":patient,
#         }
#         return render(request,"add_ppl_with_patient.html",context)
    
#     def post(self,request,*args, **kwargs):
#         form = AddPeopleWithPatientForm(request.POST)
#         if form.is_valid():
#             doctors = form.cleaned_data.get("doctor")
#             patient_doctors = DoctorModel.objects.filter(id=doctors.id)
#             print(patient_doctors)
#             print(self.get(request).context.get("doctors"))
#             print(self.get(self,request).patient)

#             for doctor in patient_doctors:
#                 instance = PeopleWithPatientModel.objects.create(doctor=doctor, patient = super(AddPplWithPatientView,self).get,is_active = True)
#                 instance.save()
#             return redirect("/")


class AddPplWithPatientView(LoginRequiredMixin,FormView):
    template_name = "add_ppl_with_patient.html"
    form_class = AddPeopleWithPatientForm
    login_url = reverse_lazy("doctor:login")


    def get_context_data(self,*args, **kwargs):
        context = super(AddPplWithPatientView,self).get_context_data(*args, **kwargs)
        patient = PatientModel.objects.get(id = self.kwargs.get("id"))
        doctors_with_patient = PeopleWithPatientModel.objects.filter(patient = patient,is_active = True)
        context["patient"] = patient
        context["doctors"] = DoctorModel.objects.filter(~Q(doctor_ppl_with_patient__in = doctors_with_patient))
        return context

    def form_valid(self,form,*args, **kwargs):
        patient = PatientModel.objects.get(id = self.kwargs.get("id"))
        doctors = form.cleaned_data.get("doctor")
        patient_doctors = DoctorModel.objects.filter(id__in=doctors)
        print(patient_doctors)
        ppl_with_patient = PeopleWithPatientModel.objects.filter(patient=patient,doctor__in=patient_doctors,is_active=False)
        print(ppl_with_patient)

        for doctor in patient_doctors:
            print(doctor)
            if PeopleWithPatientModel.objects.filter(patient=patient,doctor=doctor).exists():
                if ppl_with_patient.exists():
                    ppl_with_patient.update(is_active=True)
                    return redirect("patient:panel",patient.id)
                messages.error(self.request,"Xeta Bas Verdi.")
                return redirect("patient:add_ppl_with_patient",patient.id)

            instance = PeopleWithPatientModel.objects.create(patient = patient,is_active = True)
            instance.doctor.add(doctor)
            instance.save()
        return redirect("patient:panel",instance.patient.id,)

    def dispatch(self,request,*args, **kwargs):
        user_with_no_doctors = CustomUserModel.objects.filter(id=request.user.id,user_doctors = None,is_staff = False,is_accepted = True).first()
        if request.user.is_staff == False:
            if user_with_no_doctors:
                return redirect("doctor:create")

            elif request.user.is_accepted == False:
                return redirect("doctor:admin_permission_waiting")

            return redirect("doctor:panel",request.user.user_doctors.id)
        return super().dispatch(request,*args, **kwargs)



class ListPplWithPatientView(LoginRequiredMixin,View):
    login_url = reverse_lazy("doctor:login")

    def get(self,request,*args, **kwargs):
        user_with_no_doctors = CustomUserModel.objects.filter(id=request.user.id,user_doctors = None,is_staff = False,is_accepted = True).first()

        patient = PatientModel.objects.get(id=self.kwargs.get("id"))
        ppl_with_patient = PeopleWithPatientModel.objects.filter(patient=patient,is_active = True)
        
        if request.user.is_staff == False:
            if user_with_no_doctors:
                return redirect("doctor:create")

            elif request.user.is_accepted == False:
                return redirect("doctor:admin_permission_waiting")

            return redirect("doctor:panel",request.user.user_doctors.id)

        context = {
            "patient":patient,
            "ppl_with_patient":ppl_with_patient,
        }
        return render(request,"list_ppl_with_patient.html",context)

    def post(self,request,*args, **kwargs):
        patient = PatientModel.objects.get(id=self.kwargs.get("id"))
        doctors = self.request.POST.getlist("doctor")
        instance = PeopleWithPatientModel.objects.filter(id__in = doctors)
        for obj in instance:
            obj.is_active = False
            obj.save()
        return redirect("patient:panel",patient.id)



class PatientLogsView(LoginRequiredMixin,View):
    login_url = reverse_lazy("doctor:login")

    def get(self,request,*args, **kwargs):
        user_with_no_doctors = CustomUserModel.objects.filter(id=request.user.id,user_doctors = None,is_staff = False,is_accepted = True).first()

        patient = PatientModel.objects.get(id=self.kwargs.get("id"))

        all_operations = OperationModel.objects.filter(patient=patient)
        active_operations = OperationModel.objects.filter(patient=patient,is_active=True)
        not_active_operations = OperationModel.objects.filter(patient=patient,is_active=False)

        all_ppl_with_patient = PeopleWithPatientModel.objects.filter(patient=patient)
        active_ppl_with_patient = PeopleWithPatientModel.objects.filter(patient=patient,is_active=True)
        not_active_ppl_with_patient = PeopleWithPatientModel.objects.filter(patient=patient,is_active=False)

        notes_about_patient = PatientStatusModel.objects.filter(patient=patient).order_by("-id")
        
        if request.user.is_staff == False:
            if user_with_no_doctors:
                return redirect("doctor:create")

            elif request.user.is_accepted == False:
                return redirect("doctor:admin_permission_waiting")

            return redirect("doctor:panel",request.user.user_doctors.id)

        context = {
            "patient":patient,
            "all_operations":all_operations,
            "active_operations":active_operations,
            "not_active_operations":not_active_operations,
            "all_ppl_with_patient":all_ppl_with_patient,
            "active_ppl_with_patient":active_ppl_with_patient,
            "not_active_ppl_with_patient":not_active_ppl_with_patient,
            "notes_about_patient":notes_about_patient,
        }
        return render(request,"patient_logs.html",context)


class ActivateDeactivatePatientView(LoginRequiredMixin,View):
    login_url = reverse_lazy("doctor:login")

    def get(self, request, *args, **kwargs):
        patient = PatientModel.objects.get(id=self.kwargs.get("id"))
        user_with_no_doctors = CustomUserModel.objects.filter(id=request.user.id,user_doctors = None,is_staff = False,is_accepted = True).first()
        patient_operations = OperationModel.objects.filter(patient = patient)
        ppl_with_patient = PeopleWithPatientModel.objects.filter(patient=patient)
        
        if request.user.is_staff == True:
            if patient.is_active == True:

                for operation in patient_operations:
                    operation.is_active = False
                    operation.save()

                for obj in ppl_with_patient:
                    obj.is_active = False
                    obj.save()

                patient.is_active = False
                patient.save()
                messages.success(request,"patient deaktiv edildi")
                return redirect("patient:panel",patient.id)
            else:
                patient.is_active = True
                patient.save()
                messages.success(request,"patient aktiv edildi")
                return redirect("patient:panel",patient.id)
        else:
            if user_with_no_doctors:
                return redirect("doctor:create")

            elif request.user.is_accepted == False:
                return redirect("doctor:admin_permission_waiting")

            return redirect("doctor:panel",request.user.user_doctors.id)

