from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class TaskModel(models.Model):
    user = models.ForeignKey("account.CustomUserModel",on_delete=models.CASCADE,related_name="user_task")
    name = models.CharField(max_length=70,verbose_name="Basliq:")
    created_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    
