# Generated by Django 3.2.6 on 2022-03-29 12:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('disease', '0002_operationmodel_patient'),
    ]

    operations = [
        migrations.AlterField(
            model_name='operationmodel',
            name='finished_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
