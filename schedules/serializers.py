from rest_framework import serializers
from django.core.exceptions import ValidationError as DjangoValidationError
from drf_spectacular.utils import extend_schema_field
from .models import Schedule
from .validators import validate_cron_expression, validate_user_schedule_limit, validate_task_parameters


class ScheduleCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = ['task_definition', 'cron_expression', 'parameters', 'is_active']
    
    def validate_cron_expression(self, value):
        try:
            validate_cron_expression(value)
        except DjangoValidationError as e:
            raise serializers.ValidationError(str(e))
        return value
    
    def validate(self, attrs):
        user = self.context['request'].user
        task_definition = attrs['task_definition']
        
        try:
            validate_user_schedule_limit(user)
            validate_task_parameters(attrs['parameters'], task_definition)
        except DjangoValidationError as e:
            if hasattr(e, 'message_dict'):
                raise serializers.ValidationError(e.message_dict)
            else:
                raise serializers.ValidationError(str(e))
        
        return attrs
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        schedule = super().create(validated_data)
        
        from django_celery_beat.models import PeriodicTask, CrontabSchedule
        import json
        
        parts = schedule.cron_expression.split()
        minute, hour, day_of_month, month_of_year, day_of_week = parts
        
        crontab_schedule, created = CrontabSchedule.objects.get_or_create(
            minute=minute,
            hour=hour,
            day_of_month=day_of_month,
            month_of_year=month_of_year,
            day_of_week=day_of_week
        )
        
        PeriodicTask.objects.create(
            name=f"schedule_{schedule.id}",
            crontab=crontab_schedule,
            task=schedule.task_definition.celery_task_name,
            kwargs=json.dumps({
                'schedule_id': schedule.id,
                'parameters': schedule.parameters
            }),
            enabled=schedule.is_active
        )
        
        return schedule


class ScheduleUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = ['cron_expression', 'parameters', 'is_active']
    
    def validate_cron_expression(self, value):
        try:
            validate_cron_expression(value)
        except DjangoValidationError as e:
            raise serializers.ValidationError(str(e))
        return value
    
    def validate(self, attrs):
        task_definition = self.instance.task_definition
        parameters = attrs.get('parameters', self.instance.parameters)
        
        try:
            validate_task_parameters(parameters, task_definition)
        except DjangoValidationError as e:
            if hasattr(e, 'message_dict'):
                raise serializers.ValidationError(e.message_dict)
            else:
                raise serializers.ValidationError(str(e))
        
        return attrs
    
    def update(self, instance, validated_data):
        from django_celery_beat.models import PeriodicTask, CrontabSchedule
        import json
        
        schedule = super().update(instance, validated_data)
        
        try:
            periodic_task = PeriodicTask.objects.get(name=f"schedule_{schedule.id}")
            
            if 'cron_expression' in validated_data:
                parts = schedule.cron_expression.split()
                minute, hour, day_of_month, month_of_year, day_of_week = parts
                
                crontab_schedule, created = CrontabSchedule.objects.get_or_create(
                    minute=minute,
                    hour=hour,
                    day_of_month=day_of_month,
                    month_of_year=month_of_year,
                    day_of_week=day_of_week
                )
                periodic_task.crontab = crontab_schedule
            
            periodic_task.kwargs = json.dumps({
                'schedule_id': schedule.id,
                'parameters': schedule.parameters
            })
            periodic_task.enabled = schedule.is_active
            periodic_task.save()
            
        except PeriodicTask.DoesNotExist:
            pass
        
        return schedule


class ScheduleSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source='user.id', read_only=True)
    user_username = serializers.CharField(source='user.username', read_only=True)
    user_full_name = serializers.CharField(source='user.full_name', read_only=True)
    task_definition_id = serializers.IntegerField(source='task_definition.id', read_only=True)
    task_definition_name = serializers.CharField(source='task_definition.name', read_only=True)
    task_definition_description = serializers.CharField(source='task_definition.description', read_only=True)
    next_run_time = serializers.SerializerMethodField()
    
    class Meta:
        model = Schedule
        fields = [
            'id', 'user_id', 'user_username', 'user_full_name', 'task_definition_id',
            'task_definition_name', 'task_definition_description', 'cron_expression', 
            'parameters', 'is_active', 'created_at', 'updated_at', 'next_run_time'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    @extend_schema_field(serializers.DateTimeField(allow_null=True))
    def get_next_run_time(self, obj):
        return obj.next_run_time