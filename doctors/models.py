from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
from disease.models import OperationModel
from patients.models import PatientStatusModel, PeopleWithPatientModel
from account.models import GenderModel,BloodTypeModel
# Create your models here.


class DoctorField(models.Model):
    name = models.CharField(verbose_name="Ad:",max_length=50,null=True,blank=False)

    def __str__(self):
        return self.name
    

class DoctorModel(models.Model):

    user = models.OneToOneField("account.CustomUserModel",on_delete=models.CASCADE,null=False,blank=False,related_name="user_doctors")
    first_name = models.CharField(verbose_name="Ad:",max_length=40,null=False,blank=False)
    last_name = models.CharField(verbose_name="Soyad:",max_length=60,null=False,blank=False)
    gender = models.ForeignKey(GenderModel,max_length=6,null=True,blank=False,on_delete=models.SET_NULL)
    working_field = models.ForeignKey(DoctorField,on_delete=models.SET_NULL,null=True,blank=False,related_name="field_doctors")
    phonenumber = PhoneNumberField(null=False,blank=True)
    about = models.TextField(verbose_name="Haqqinda:",null=True,blank=True)
    is_active = models.BooleanField(default=True)
    blood_type=models.ForeignKey(BloodTypeModel,max_length=10, null=True,blank=False,on_delete=models.SET_NULL)
    born_date = models.DateField(null=True,blank=False)

    def get_full_name(self):
        return self.first_name + ' ' + self.last_name


    def __str__(self):
        return self.first_name + " " + self.last_name
    

