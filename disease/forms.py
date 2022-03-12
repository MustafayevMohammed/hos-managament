from django import forms
from disease.models import OperationModel

class CreateOperationForm(forms.Form):

    class Meta:
        model = OperationModel
        fields = ["name","description","disease","doctor","patient"]
