from django.db import models
import uuid
from django.contrib.auth import get_user_model
from django import forms
# Create your models here.
User = get_user_model()

class Manager(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    id = models.UUIDField(primary_key=True, default= uuid.uuid4, editable = False)
    phone_number = models.CharField(max_length=12, null=True)
    GD = (
        ('male', 'Male'),
        ('female', 'Female'),
        ('others', 'Others'),
        ('not specify', 'Do not wish to specify')
    )

    gender = models.CharField(choices=GD, max_length=400, default=None, null=False)

    CT = (
        ('manager', 'Manager'),
        ('task-manager', 'Task Manager')
    )

    category = models.CharField(choices=CT, max_length=250, default=None, null = False)
    def __str__(self):
        return str(self.id)

    def save(self, *args, **kwargs):
        super(Manager, self).save(*args, **kwargs)
