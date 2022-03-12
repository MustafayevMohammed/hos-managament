from django.contrib import admin
from . models import PatientModel, PatientStatusModel, PeopleWithPatientModel, BloodTypeModel, GenderModel
# Register your models here.

admin.site.register(PatientModel)
admin.site.register(PatientStatusModel)
admin.site.register(PeopleWithPatientModel)
admin.site.register(BloodTypeModel)
admin.site.register(GenderModel)