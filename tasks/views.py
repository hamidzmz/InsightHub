from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from drf_spectacular.utils import extend_schema
from .models import TaskDefinition
from .serializers import TaskDefinitionSerializer


class TaskDefinitionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = TaskDefinition.objects.filter(is_active=True)
    serializer_class = TaskDefinitionSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ['name', 'is_active']
    ordering_fields = ['name', 'created_at']
    search_fields = ['name', 'description']
    ordering = ['name']
    
    @extend_schema(
        responses={200: TaskDefinitionSerializer(many=True)}
    )
    @action(detail=False, methods=['get'])
    def available(self, request):
        tasks = self.get_queryset()
        serializer = self.get_serializer(tasks, many=True)
        return Response({
            'count': tasks.count(),
            'tasks': serializer.data
        })