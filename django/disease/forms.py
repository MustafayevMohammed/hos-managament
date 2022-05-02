from django import forms
from disease.models import OperationModel

class CreateOperationForm(forms.ModelForm):

    class Meta:
        model = OperationModel
        fields = ["name","description","disease","doctor","patient"]
