# Generated by Django 2.2.2 on 2019-06-30 07:57

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('manager_login', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='manager',
            name='id',
            field=models.UUIDField(default=uuid.UUID('3213f287-4abb-4fd2-85c8-7b313b73cd25'), editable=False, primary_key=True, serialize=False),
        ),
    ]