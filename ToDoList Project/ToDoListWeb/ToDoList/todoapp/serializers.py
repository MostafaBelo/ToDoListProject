from rest_framework import serializers

from .models import data
from django.contrib.auth.models import User

class dataSerializer(serializers.ModelSerializer):
    class Meta:
        model = data
        fields = ['id','task','duedate','person','done', 'task_user']

class userSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'email']