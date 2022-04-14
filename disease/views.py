from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from account.models import CustomUserModel
from disease.models import DiseaseModel, OperationModel
from django.contrib.auth.mixins import LoginRequiredMixin
from doctors.models import DoctorModel
from django.views.generic import CreateView
from disease.forms import CreateOperationForm
from patients.models import PatientModel, PeopleWithPatientModel
from django.contrib import messages
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

class OperationCreateView(LoginRequiredMixin,CreateView):
    template_name = "create_operation.html"
    form_class = CreateOperationForm
    login_url = reverse_lazy("doctor:login")

    def get_context_data(self,*args, **kwargs):
        context = super().get_context_data(**kwargs)
        context["diseases"] = DiseaseModel.objects.all()
        context["doctors"] = DoctorModel.objects.all()
        context["patients"] = PatientModel.objects.filter(is_active = True)
        return context
    
    
    def form_valid(self,form,*args, **kwargs):
        name = form.cleaned_data.get("name")
        patient = form.cleaned_data.get("patient")
        description = form.cleaned_data.get("description")

        form_diseases = form.cleaned_data.get("disease")
        form_doctors = form.cleaned_data.get("doctor")

        diseases = DiseaseModel.objects.filter(id__in = form_diseases)
        doctors = DoctorModel.objects.filter(id__in = form_doctors)
        unactive_ppl_with_patient = PeopleWithPatientModel.objects.filter(patient = patient, doctor__in = doctors,is_active = False)

        ppl_with_not_patient = DoctorModel.objects.exclude(
            doctor_ppl_with_patient__patient = patient,
        )

        if unactive_ppl_with_patient.exists():
            unactive_ppl_with_patient.update(is_active = True)
            
        instance = OperationModel.objects.create(name = name, patient = patient, description = description)
        instance.disease.add(*diseases)
        instance.doctor.add(*doctors)
        for doctor in ppl_with_not_patient:
            obj = PeopleWithPatientModel.objects.create(patient = patient, is_active = True)
            obj.doctor.add(doctor)
        return redirect("disease:panel",instance.id)


class ActivateDeactivateOperation(LoginRequiredMixin,View):
    login_url = reverse_lazy("doctor:login")

    def get(self,request,*args, **kwargs):
        operation = OperationModel.objects.get(id = kwargs.get("id"))
        user_with_no_doctors = CustomUserModel.objects.filter(id=request.user.id,user_doctors = None,is_staff = False,is_accepted = True).first()


        if request.user.is_staff == True:
            if operation.is_active == True:
                operation.is_active = False
                operation.save()
                
                return redirect("disease:panel",operation.id)
            
            else:
                operation.is_active = True
                operation.save()
                return redirect("disease:panel",operation.id)
        else:
            if user_with_no_doctors.exists():
                return redirect("doctor:create")

            elif request.user.is_accepted == False:
                return redirect("doctor:admin_permission_waiting")

            return redirect("doctor:panel",request.user.user_doctors.id)
            

class ActiveOperationsListView(LoginRequiredMixin,View):

    login_url = reverse_lazy("doctor:login")

    def get(self,request,*args, **kwargs):

        user_with_no_doctors = CustomUserModel.objects.filter(id=request.user.id,user_doctors = None,is_staff = False,is_accepted = True).first()
        operations = OperationModel.objects.filter(is_active = True)

        if request.user.is_staff == False:
            if user_with_no_doctors:
                return redirect("doctor:create")
            
            if request.user.is_accepted == False:
                return redirect("doctor:admin_permission_waiting")
            
            return redirect("doctor:panel",request.user.user_doctors.id)
        
        context = {
            "operations":operations,
        }
        return render(request,"list_of_operations.html",context)


    def post(self,request,*args, **kwargs):
        form_operations = self.request.POST.getlist("operation")
        instance = OperationModel.objects.filter(id__in = form_operations)

        for obj in instance:
            obj.is_active = False
            obj.save()
        messages.success(request,"Emeliyyatlar Ugurla Deaktiv Oldu!")
        return redirect("disease:active_operations")