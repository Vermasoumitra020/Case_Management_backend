from django.shortcuts import render
from .serializers import ManagerRegistrationSerializers, ManagerLoginSerializers
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from .models import Manager
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from django.contrib.auth import login as django_login, logout as django_logout
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
import json
from django.shortcuts import render
from django.core import serializers
from django.contrib.auth.models import User
from manager_app.models import Tasks
from django.core.serializers.json import DjangoJSONEncoder
from django.forms.models import model_to_dict

# Create your views here.
# @api_view(['POST'])
@permission_classes((AllowAny,))
class ManagerSignupView(APIView):
    def post(self, request):
        manager_signup_serializer = ManagerRegistrationSerializers(data = request.data, many=False)
        if manager_signup_serializer.is_valid():
            manager_signup_serializer.save()

            return Response(manager_signup_serializer.data, status = status.HTTP_201_CREATED)
        else:
            return Response(manager_signup_serializer.errors, status = status.HTTP_400_BAD_REQUEST)

@permission_classes((AllowAny,))
class ManagerLoginView(APIView):
    # authentication_classes = SessionAuthentication
    # permission_classes = (IsAuthenticated,)
    def post(self, request):
        tasks = []

        login_serializer = ManagerLoginSerializers(data = request.data)
        login_serializer.is_valid(raise_exception=True)
        user = login_serializer.validated_data['user']
        django_login(request, user)
        token, created = Token.objects.get_or_create(user = user)

        user_new = list(User.objects.filter(id= request.user.id).values("username", "first_name", "last_name", "email"))
        manager_data = list(Manager.objects.filter(user = request.user).values("id", "category"))

        if manager_data[0]["category"] == 'manager':
            tasks = list(Tasks.objects.all().values("id","task_subject", "starting_date", "end_date", "status"))
        elif manager_data[0]["category"] == 'task-manager':
            tasks = list(Tasks.objects.filter(work_to = manager_data[0]["id"]).values("id", "task_subject", "starting_date", "end_date", "status"))

        for i in range(len(tasks)):
            tasks[i]["starting_date"] = tasks[i]["starting_date"]
            tasks[i]["end_date"] = tasks[i]["end_date"]

        # print(jwt.decode(token, "SECRET", algorithms=["HS256"]))
        task_manager_list = list(Manager.objects.filter(category='task-manager').values("user", 'id'))
        for i in range(len(task_manager_list)):
            user_name = list(User.objects.filter(id = task_manager_list[i]["user"]).values("username"))
            id = task_manager_list[i]['id']
            task_manager_list[i]["user"] = user_name[0]["username"]
            task_manager_list[i]["id"] = id

        if created:
            json_data = {}
            if manager_data[0]["category"] == 'manager':
                json_data = {
                    "username": user_new[0]["username"],
                    "id": manager_data[0]["id"],
                    "first_name": user_new[0]["first_name"],
                    "last_name": user_new[0]["last_name"],
                    "email": user_new[0]["email"],
                    "category": manager_data[0]["category"],
                    "task_data": tasks,
                    "task_manager_list" : task_manager_list,
                    "token": token.key
                }
            else:
                json_data = {
                    "username": user_new[0]["username"],
                    "id": manager_data[0]["id"],
                    "first_name": user_new[0]["first_name"],
                    "last_name": user_new[0]["last_name"],
                    "email": user_new[0]["email"],
                    "category": manager_data[0]["category"],
                    "task_data": tasks,
                    "token": token.key
                }
            return Response(json_data, status = status.HTTP_201_CREATED)

        return Response(login_serializer.errors, status=status.HTTP_401_UNAUTHORIZED)



class ManagerLogoutView(APIView):
    authentication_classes = (TokenAuthentication,)
    def post(self, request):
        # trying to logout the user
        request.user.auth_token.delete()
        django_logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)



