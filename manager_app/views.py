from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import TaskSerializers
from rest_framework import status
from .models import Tasks
from rest_framework import exceptions
from django.http import JsonResponse
from manager_login.models import Manager
from rest_framework import serializers
import json
from django.core.serializers.json import DjangoJSONEncoder
from rest_framework.mixins import UpdateModelMixin, DestroyModelMixin
from .serializers import UpdateViewSerializer

# Create your views here.
class TaskViews(APIView):
    def get(self, request):
        d = Manager.objects.filter(category='task-manager').values()
        return Response({"results" : list(d)})

    def post(self, request):
        instance = request.data["work_to"]
        taskserializer = TaskSerializers(data = request.data, context={"instance" : instance})
        if taskserializer.is_valid():
            taskserializer.save()
            return Response(taskserializer.data, status=status.HTTP_201_CREATED)
        return Response(taskserializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ViewTaskView(APIView):
    def post(self, request):
        id = request.data["id"]
        instance = Manager.objects.get(id=id)
        tasks = Tasks.objects.filter(work_to = instance).values("id", "task_subject", "task_details", "starting_date", "end_date", "status")

        return JsonResponse(list(tasks), safe=False)

class DeleteTaskView(APIView):
    def delete(self, request, factory_id):
        id = request.data.get("id") if "id" in request.data else None
        if id:
            obj = Tasks.objects.filter(id = id)
            obj.delete()
            return Response(status=status.HTTP_410_GONE)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class UpdateTaskView(APIView):
    data = Tasks.objects.all()
    serializer = UpdateViewSerializer

    def put(self, request):
        id = request.data.get("id")
        snippet = Tasks.objects.get(id = id)
        data = request.data
        serializer = UpdateViewSerializer(snippet, data = data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
