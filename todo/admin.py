from django.contrib import admin
from . models import TaskModel, TestModel
# Register your models here.

admin.site.register(TaskModel)

admin.site.register(TestModel)