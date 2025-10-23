# users/views.py

from rest_framework import generics
from django.contrib.auth import get_user_model  # ✅ Use this instead of importing User directly
from rest_framework.permissions import AllowAny
from .serializers import RegisterSerializer

User = get_user_model()  # ✅ Dynamically fetch your active user model

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]  # Allow anyone to register
