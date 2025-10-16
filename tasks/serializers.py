from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')  # shows username of owner

    class Meta:
        model = Task
        fields = ['id', 'owner', 'title', 'description', 'is_completed', 'completed_at', 'priority', 'created_at', 'due_date']
        read_only_fields = ['id', 'owner', 'created_at', 'completed_at']
