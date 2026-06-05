# serializers.py
from rest_framework import serializers
from .models import Task # Ensure this matches your model name

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        # Change 'is_completed' to 'status'
        fields = ['id', 'title', 'description', 'deadline', 'status', 'category', 'priority']