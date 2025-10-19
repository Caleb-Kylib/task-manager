from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone

from .models import Task
from .serializers import TaskSerializer, UserSerializer
from .permissions import IsOwner
from django.contrib.auth.models import User


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'due_date', 'priority']

    def get_queryset(self):
        # Only show tasks belonging to the logged-in user
        qs = Task.objects.filter(owner=self.request.user)

        # Filtering: status (pending/completed), priority, due_date
        status_param = self.request.query_params.get('status')
        if status_param:
            if status_param.lower() == 'completed':
                qs = qs.filter(is_completed=True)
            elif status_param.lower() == 'pending':
                qs = qs.filter(is_completed=False)

        priority_param = self.request.query_params.get('priority')
        if priority_param:
            try:
                p = int(priority_param)
                qs = qs.filter(priority=p)
            except ValueError:
                # ignore invalid priority filter
                pass

        due_date_param = self.request.query_params.get('due_date')
        if due_date_param:
            # Expecting yyyy-mm-dd or partial match; do a startswith on isoformat
            qs = qs.filter(due_date__date=due_date_param)

        # Ordering: allow ordering by due_date or priority via ?ordering=due_date or ?ordering=-priority
        return qs

    def perform_create(self, serializer):
        # Automatically assign owner to the logged-in user
        serializer.save(owner=self.request.user)

    def update(self, request, *args, **kwargs):
        # Prevent editing a completed task unless the update is marking it incomplete
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        # If task is completed and request does not attempt to set is_completed to False, block
        if instance.is_completed:
            incoming_is_completed = request.data.get('is_completed')
            if incoming_is_completed in [None, '', 'true', 'True', True]:
                return Response({'detail': 'Completed tasks cannot be edited. Revert to incomplete first.'}, status=status.HTTP_400_BAD_REQUEST)

        return super().update(request, *args, **kwargs)

    @action(detail=True, methods=['post'], url_path='mark')
    def mark(self, request, pk=None):
        """Mark a task complete or incomplete.

        POST body: { "is_completed": true } or { "is_completed": false }
        """
        task = self.get_object()
        is_completed = request.data.get('is_completed')
        if is_completed is None:
            return Response({'detail': 'is_completed is required'}, status=status.HTTP_400_BAD_REQUEST)

        # Normalize boolean-like inputs
        if isinstance(is_completed, str):
            is_completed = is_completed.lower() in ['1', 'true', 'yes', 'y']

        if is_completed:
            # mark complete
            task.is_completed = True
            task.completed_at = timezone.now()
            task.save()
            return Response({'detail': 'Task marked complete', 'completed_at': task.completed_at}, status=status.HTTP_200_OK)
        else:
            # mark incomplete
            task.is_completed = False
            task.completed_at = None
            task.save()
            return Response({'detail': 'Task marked incomplete'}, status=status.HTTP_200_OK)


class UserViewSet(viewsets.ModelViewSet):
    """Basic User CRUD viewset.

    - Anyone may create a new user (registration).
    - Authenticated users may view/update their own profile.
    - Staff users may list all users.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        # Allow unauthenticated create (registration)
        if self.action == 'create':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        # Staff can list all; regular users only see themselves
        user = self.request.user
        if user.is_staff:
            return User.objects.all()
        return User.objects.filter(pk=user.pk)


