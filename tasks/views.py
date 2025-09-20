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
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)