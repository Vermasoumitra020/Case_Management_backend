from django.db import models
from django.contrib.auth.models import User
from manager_login.models import Manager
import uuid
# Create your models here.
class Tasks(models.Model):
    work_to = models.ForeignKey(Manager,
                                on_delete=models.CASCADE,
                                limit_choices_to={'category' : 'task-manager'})

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    task_subject = models.CharField(max_length=250)
    task_details = models.CharField(max_length=500)
    starting_date = models.DateField(auto_created=True)
    end_date = models.DateField()
    st = (
        ('completed', 'Complete'),
        ('pending', 'Pending')
    )
    status = models.CharField(max_length=150, choices=st, default='pending')

    def __str__(self):
        return self.task_subject

