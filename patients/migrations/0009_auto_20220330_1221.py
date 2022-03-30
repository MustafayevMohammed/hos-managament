# Generated by Django 3.2.6 on 2022-03-30 08:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('doctors', '0003_auto_20220330_1221'),
        ('account', '0002_bloodtypemodel_gendermodel'),
        ('patients', '0008_alter_peoplewithpatientmodel_doctor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patientmodel',
            name='blood_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.bloodtypemodel'),
        ),
        migrations.AlterField(
            model_name='patientmodel',
            name='gender',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.gendermodel'),
        ),
        migrations.DeleteModel(
            name='BloodTypeModel',
        ),
        migrations.DeleteModel(
            name='GenderModel',
        ),
    ]
