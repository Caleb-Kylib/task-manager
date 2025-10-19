from rest_framework import serializers
from django.utils import timezone
from django.contrib.auth.models import User
from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    """Serializer for Task model."""
    owner = serializers.ReadOnlyField(source='owner.username')  # Show username of task owner

    class Meta:
        model = Task
        fields = [
            'id',
            'owner',
            'title',
            'description',
            'is_completed',
            'completed_at',
            'priority',
            'created_at',
            'due_date'
        ]
        read_only_fields = ['id', 'owner', 'created_at', 'completed_at']

    def validate_due_date(self, value):
        """Ensure due_date, if provided, is in the future (timezone-aware)."""
        if value and value <= timezone.now():
            raise serializers.ValidationError("Due date must be in the future.")
        return value


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for user creation and profile management.
    - Password is write-only and will be hashed automatically.
    - Email uniqueness is validated (case-insensitive).
    """
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        read_only_fields = ['id']

    def validate_email(self, value):
        if value and User.objects.filter(email__iexact=value).exclude(pk=getattr(self.instance, 'pk', None)).exists():
            raise serializers.ValidationError("A user with that email already exists.")
        return value

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        """Ensure password updates are hashed."""
        password = validated_data.pop('password', None)
        for attr, val in validated_data.items():
            setattr(instance, attr, val)
        if password:
            instance.set_password(password)
        instance.save()
        return instance
