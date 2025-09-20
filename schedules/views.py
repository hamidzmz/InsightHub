from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from drf_spectacular.utils import extend_schema
from django_celery_beat.models import PeriodicTask
from .models import Schedule
from .serializers import ScheduleSerializer, ScheduleCreateSerializer, ScheduleUpdateSerializer
from executions.models import ExecutionLog
from executions.serializers import ExecutionLogSerializer
from api.permissions import IsOwnerOrSuperUser
from api.filters import ScheduleFilter


class ScheduleViewSet(viewsets.ModelViewSet):
    queryset = Schedule.objects.select_related('user', 'task_definition').all()
    serializer_class = ScheduleSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrSuperUser]
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_class = ScheduleFilter
    ordering_fields = ['created_at', 'updated_at', 'is_active']
    search_fields = ['task_definition__name']
    ordering = ['-created_at']
    
    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Schedule.objects.select_related('user', 'task_definition').all()
        return Schedule.objects.select_related('user', 'task_definition').filter(user=user)
    
    def get_serializer_class(self):
        if self.action == 'create':
            return ScheduleCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return ScheduleUpdateSerializer
        return ScheduleSerializer

    def create(self, request, *args, **kwargs):
        create_serializer = ScheduleCreateSerializer(data=request.data, context=self.get_serializer_context())
        create_serializer.is_valid(raise_exception=True)
        instance = create_serializer.save()
        read_serializer = ScheduleSerializer(instance, context=self.get_serializer_context())
        return Response(read_serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        update_serializer = ScheduleUpdateSerializer(instance, data=request.data, partial=partial, context=self.get_serializer_context())
        update_serializer.is_valid(raise_exception=True)
        instance = update_serializer.save()
        read_serializer = ScheduleSerializer(instance, context=self.get_serializer_context())
        return Response(read_serializer.data)

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)
    
    @extend_schema(
        responses={200: ExecutionLogSerializer(many=True)}
    )
    @action(detail=True, methods=['get'])
    def logs(self, request, pk=None):
        schedule = self.get_object()
        executions = ExecutionLog.objects.select_related('schedule', 'schedule__user', 'schedule__task_definition').filter(schedule=schedule).order_by('-started_at')
        
        page = self.paginate_queryset(executions)
        if page is not None:
            serializer = ExecutionLogSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = ExecutionLogSerializer(executions, many=True)
        return Response(serializer.data)
    
    @extend_schema(
        request=None,
        responses={200: {'type': 'object', 'properties': {'message': {'type': 'string'}}}}
    )
    @action(detail=True, methods=['post'])
    def toggle_active(self, request, pk=None):
        schedule = self.get_object()
        schedule.is_active = not schedule.is_active
        schedule.save()
        
        try:
            periodic_task = PeriodicTask.objects.get(name=f"schedule_{schedule.id}")
            periodic_task.enabled = schedule.is_active
            periodic_task.save()
        except PeriodicTask.DoesNotExist:
            pass
        
        action_text = "activated" if schedule.is_active else "deactivated"
        return Response({
            'message': f'Schedule {action_text} successfully',
            'is_active': schedule.is_active
        })
    
    @extend_schema(
        request={
            'type': 'object',
            'properties': {
                'filters': {'type': 'object'},
                'ordering': {'type': 'array', 'items': {'type': 'string'}},
                'page_size': {'type': 'integer'}
            }
        },
        responses={200: ScheduleSerializer(many=True)}
    )
    @action(detail=False, methods=['post'])
    def search(self, request):
        queryset = self.get_queryset()
        from api.filters import DynamicFilterBackend
        queryset = DynamicFilterBackend().filter_queryset(request, queryset, self)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    def perform_destroy(self, instance):
        try:
            periodic_task = PeriodicTask.objects.get(name=f"schedule_{instance.id}")
            periodic_task.delete()
        except PeriodicTask.DoesNotExist:
            pass
        instance.delete()