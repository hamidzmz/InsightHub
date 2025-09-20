from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from croniter import croniter
from tasks.models import TaskDefinition

User = get_user_model()


class Schedule(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='schedules')
    task_definition = models.ForeignKey(TaskDefinition, on_delete=models.CASCADE, related_name='schedules')
    cron_expression = models.CharField(max_length=100)
    parameters = models.JSONField(default=dict)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'schedules'
        indexes = [
            models.Index(fields=['user', 'is_active']),
            models.Index(fields=['task_definition']),
            models.Index(fields=['created_at']),
        ]
        ordering = ['-created_at']
        
    def __str__(self):
        return f"{self.user.username} - {self.task_definition.name}"
        
    def clean(self):
        if not croniter.is_valid(self.cron_expression):
            raise ValidationError({'cron_expression': 'Invalid cron expression'})
        
        if not self.user.is_superuser:
            active_count = Schedule.objects.filter(
                user=self.user, 
                is_active=True
            ).exclude(pk=self.pk).count()
            if active_count >= 5:
                raise ValidationError('Regular users cannot have more than 5 active jobs')
        
        parameter_errors = self.task_definition.validate_parameters(self.parameters)
        if parameter_errors:
            raise ValidationError({'parameters': parameter_errors})
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
        
    @property
    def next_run_time(self):
        from django.utils import timezone
        import datetime
        cron = croniter(self.cron_expression, timezone.now())
        next_dt = cron.get_next(datetime.datetime)
        if timezone.is_naive(next_dt):
            next_dt = timezone.make_aware(next_dt, timezone.get_current_timezone())
        return next_dt