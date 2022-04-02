from django import forms
from doctors.models import DoctorModel


class DoctorForm(forms.ModelForm):
    
    class Meta:
        model = DoctorModel
        fields = ["first_name", "last_name", "gender", "working_field", "phonenumber", "about", "blood_type", "born_date"]