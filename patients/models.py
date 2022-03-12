from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
# from disease.models import DiseaseModel

# Create your models here.

class PatientModel(models.Model):

    BLOOD_TYPE_CHOICES = [
        ("A+","A+"),
        ("A-","A-"),
        ("B+","B+"),
        ("B-","B-"),
        ("O+","O+"),
        ("O-","O-"),
        ("AB+","AB+"),
        ("AB-","AB-"),
    ]

    GENDER_CHOICES = [
        ("Male","Male"),
        ("Female","Female"),
    ]

    first_name = models.CharField(max_length=30, verbose_name="Ad:",null=False,blank=False)
    last_name = models.CharField(max_length=40,verbose_name="Soyadi:",null=False,blank=False)
    gender = models.CharField(choices=GENDER_CHOICES,max_length=6)
    phonenumber = PhoneNumberField(blank=True,null=True,unique=True)
    joining_date = models.DateTimeField(auto_now_add=True,verbose_name="Giris Tarixi:")
    expected_discharging_date = models.DateTimeField(verbose_name="Gozlenilen Cixis Tarixi:",null=True,blank=True)
    discharged_date = models.DateTimeField(verbose_name="Cixis Tarixi:",null=True,blank=True)
    born_date = models.DateField(verbose_name="Dogum Tarixi:")
    blood_type = models.CharField(choices=BLOOD_TYPE_CHOICES,max_length=10)
    additional_information = models.TextField(null=True,blank=True)
    disease = models.ManyToManyField("disease.DiseaseModel",related_name="disease_patients")
    is_active = models.BooleanField(default=True)

    def get_full_name(self):
        return self.first_name + ' ' + self.last_name

    def __str__(self):
        return self.first_name + " " + self.last_name
    


class PatientStatusModel(models.Model):
    
    STATUS_CHOICES = [
        ("Yaxsi","Yaxsi"),
        ("Stabil","Stabil"),
        ("Agir","Agir"),
        ("Emeliyyata_Hazirlasir","Emeliyyata Hazirlasir"),
        ("Emeliyyatdadir","Emeliyyatdadir"),
    ]
    

    patient = models.ForeignKey(PatientModel, on_delete = models.CASCADE,null=True,blank=False,default=1,related_name="patient_status")
    status = models.CharField(choices=STATUS_CHOICES,max_length=22)
    note = models.TextField(verbose_name="Xestenin cari veziyyeti haqqinda melumat:")
    date = models.DateTimeField(auto_now_add=True,verbose_name="Gun Ve Vaxt:")
    doctor = models.ForeignKey("doctors.DoctorModel",null=True,blank=False,on_delete=models.SET_NULL)




class PeopleWithPatientModel(models.Model):
    patient = models.ForeignKey("patients.PatientModel",on_delete=models.CASCADE,related_name="patient_ppl_with_patient")
    doctor = models.ForeignKey("doctors.DoctorModel",related_name="doctor_ppl_with_patient", on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)