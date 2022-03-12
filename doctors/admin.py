from django.contrib import admin
from . models import DoctorField, DoctorModel
# Register your models here.

admin.site.register(DoctorField)
admin.site.register(DoctorModel)
