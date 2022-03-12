# Generated by Django 3.2.6 on 2022-03-12 15:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('patients', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BloodTypeModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='GenderModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.AlterField(
            model_name='patientmodel',
            name='blood_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='patients.bloodtypemodel'),
        ),
        migrations.AlterField(
            model_name='patientmodel',
            name='gender',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='patients.gendermodel'),
        ),
    ]
