from .models import Manager
from rest_framework import serializers
from rest_framework import exceptions
from django.contrib.auth import authenticate
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User

class ManagerRegistrationSerializers(serializers.Serializer):
    username = serializers.CharField(max_length=250, required = True, validators=[UniqueValidator(queryset=User.objects.all())])
    first_name = serializers.CharField(max_length=250, required= False)
    last_name = serializers.CharField(max_length=250, required= False)
    email = serializers.EmailField(max_length=250, required=True, validators=[UniqueValidator(queryset=User.objects.all())])
    phone_no = serializers.CharField(max_length=250, required=False, validators=[UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(max_length=250 ,required=True)
    gender = serializers.CharField(max_length=20, default= 'male',required=False)
    category = serializers.CharField(max_length=20, default= 'manager',required=False)

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'],
                                        first_name = validated_data['first_name'],
                                        last_name = validated_data['last_name'],
                                        email = validated_data['email'],
                                        password = validated_data['password'])

        print(validated_data)
        Manager.objects.create(user = user,
                               # phone_no=validated_data['phone_no'],
                                gender = validated_data['gender'],
                                category=validated_data['category'])

        return user

    class Meta:
        model = Manager
        fields = ('username', 'email', 'first_name', 'last_name', 'email', 'phone_no', 'password', 'gender', 'category'  ,'password')
#



class ManagerLoginSerializers(serializers.Serializer):
    username = serializers.CharField(max_length=250)
    password = serializers.CharField(max_length=250)

    def validate(self, data):
        username = data.get('username', '')
        password = data.get('password', '')
        if username and password:
            user = authenticate(username = username, password = password)
            if user:
                if user.is_active:
                    data['user'] = user
            else:
                raise exceptions.ValidationError("Wrong username or password")
        else:
            raise exceptions.ValidationError("Username and Password are required")

        return data