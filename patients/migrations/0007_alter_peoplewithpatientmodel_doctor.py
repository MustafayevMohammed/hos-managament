# Generated by Django 3.2.6 on 2022-03-27 16:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctors', '0001_initial'),
        ('patients', '0006_auto_20220327_1909'),
    ]

    operations = [
        migrations.AlterField(
            model_name='peoplewithpatientmodel',
            name='doctor',
            field=models.ManyToManyField(blank=True, related_name='doctor_ppl_with_patient', to='doctors.DoctorModel'),
        ),
    ]
