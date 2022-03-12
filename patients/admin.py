from django.contrib import admin
from . models import PatientModel, PatientStatusModel, PeopleWithPatientModel
# Register your models here.

admin.site.register(PatientModel)
admin.site.register(PatientStatusModel)
admin.site.register(PeopleWithPatientModel)