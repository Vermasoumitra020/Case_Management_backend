from rest_framework import serializers
from .models import Tasks
from manager_login.models import Manager

from datetime import *
from django.contrib.auth.models import User

class TaskSerializers(serializers.Serializer):
    work_to = serializers.UUIDField(format='hex_verbose')
    task_subject = serializers.CharField(max_length=250)
    task_details = serializers.CharField(max_length=500)
    starting_date = serializers.DateField()
    end_date = serializers.DateField()
    status = serializers.CharField(max_length=100)


    def create(self, validated_data):
        id = self.context.get("instance")
        task_details = Tasks.objects.create(work_to = Manager(id=id),
                                            task_subject = validated_data["task_subject"],
                                            task_details = validated_data["task_details"],
                                            starting_date = validated_data["starting_date"],
                                            end_date = validated_data["end_date"],
                                            status = validated_data["status"])

        return task_details

    class Meta:
        model = Manager
        fields = "__all__"


class UpdateViewSerializer(serializers.Serializer):
    status = serializers.CharField(max_length=100, required=False)
    end_date = serializers.DateField(required=False)
    task_details = serializers.CharField(max_length=500, required=False)
    task_subject = serializers.CharField(max_length=250, required=False)

    def update(self, instance, validated_data):
        instance.status = validated_data.get('status', instance.status)
        instance.task_subject = validated_data.get('task_subject', instance.task_subject)
        instance.task_details = validated_data.get('task_details', instance.task_details)
        instance.end_date = validated_data.get('end_date', instance.end_date)
        instance.save()
        return instance


