from django.db import models
# Create your models here.

class DiseaseModel(models.Model):
    name = models.CharField(max_length=30,verbose_name="Xesteliyin Adi:")
    
    def __str__(self):
        return self.name


class OperationModel(models.Model):
    name = models.CharField(null=True,blank=True,max_length=45)
    description = models.TextField(null=True,blank=True)
    disease = models.ManyToManyField(DiseaseModel,related_name="disease_operations")
    doctor = models.ManyToManyField("doctors.DoctorModel",blank=False,related_name="doctor_operations")
    starting_date = models.DateTimeField(auto_now_add=True)
    finished_date = models.DateTimeField(auto_now=True)
    patient = models.ForeignKey("patients.PatientModel",on_delete=models.DO_NOTHING,related_name="patient_operations")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    