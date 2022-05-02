from django.contrib import admin
from . models import DiseaseModel, OperationModel

# Register your models here.
admin.site.register(DiseaseModel)
admin.site.register(OperationModel)