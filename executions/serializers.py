from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field
from .models import ExecutionLog


class ExecutionLogSerializer(serializers.ModelSerializer):
    schedule_id = serializers.IntegerField(source='schedule.id', read_only=True)
    task_name = serializers.CharField(source='schedule.task_definition.name', read_only=True)
    user_username = serializers.CharField(source='schedule.user.username', read_only=True)
    duration_seconds = serializers.SerializerMethodField()
    is_completed = serializers.SerializerMethodField()
    
    class Meta:
        model = ExecutionLog
        fields = [
            'id', 'schedule_id', 'task_name', 'user_username', 'celery_task_id', 'status', 
            'started_at', 'completed_at', 'result', 'error_message', 'execution_time',
            'duration_seconds', 'is_completed'
        ]
        read_only_fields = ['id', 'started_at', 'completed_at', 'execution_time']
    
    @extend_schema_field(serializers.FloatField(allow_null=True))
    def get_duration_seconds(self, obj):
        return obj.duration_seconds
    
    @extend_schema_field(serializers.BooleanField())
    def get_is_completed(self, obj):
        return obj.is_completed


class ExecutionLogDetailSerializer(serializers.ModelSerializer):
    schedule_id = serializers.IntegerField(source='schedule.id', read_only=True)
    schedule_cron = serializers.CharField(source='schedule.cron_expression', read_only=True)
    task_name = serializers.CharField(source='schedule.task_definition.name', read_only=True)
    task_description = serializers.CharField(source='schedule.task_definition.description', read_only=True)
    user_username = serializers.CharField(source='schedule.user.username', read_only=True)
    user_full_name = serializers.CharField(source='schedule.user.full_name', read_only=True)
    duration_seconds = serializers.SerializerMethodField()
    is_completed = serializers.SerializerMethodField()
    
    class Meta:
        model = ExecutionLog
        fields = [
            'id', 'schedule_id', 'schedule_cron', 'task_name', 'task_description',
            'user_username', 'user_full_name', 'celery_task_id', 'status',
            'started_at', 'completed_at', 'result', 'error_message', 'execution_time',
            'duration_seconds', 'is_completed'
        ]
        read_only_fields = ['id', 'started_at', 'completed_at', 'execution_time']
    
    @extend_schema_field(serializers.FloatField(allow_null=True))
    def get_duration_seconds(self, obj):
        return obj.duration_seconds
    
    @extend_schema_field(serializers.BooleanField())
    def get_is_completed(self, obj):
        return obj.is_completed