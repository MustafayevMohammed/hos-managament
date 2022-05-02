from django import forms
from patients.models import PatientModel, PatientStatusModel, PeopleWithPatientModel

class CreatePatientForm(forms.ModelForm):

    class Meta:
        model = PatientModel
        exclude = ["is_active"]


class AddPatientStatusForm(forms.ModelForm):

    class Meta:
        model = PatientStatusModel
        fields = ["status", "note"]


class AddPeopleWithPatientForm(forms.ModelForm):

    class Meta:
        model = PeopleWithPatientModel
        fields = ["doctor"]