from django.db import models
from django.utils import timezone
from schedules.models import Schedule


class ExecutionLog(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('running', 'Running'),
        ('success', 'Success'),
        ('failure', 'Failure'),
        ('retry', 'Retry'),
    ]
    
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE, related_name='executions')
    celery_task_id = models.CharField(max_length=255, unique=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    started_at = models.DateTimeField()
    completed_at = models.DateTimeField(null=True, blank=True)
    result = models.JSONField(null=True, blank=True)
    error_message = models.TextField(null=True, blank=True)
    execution_time = models.DurationField(null=True, blank=True)
    
    class Meta:
        db_table = 'execution_logs'
        indexes = [
            models.Index(fields=['schedule', 'started_at']),
            models.Index(fields=['status']),
            models.Index(fields=['celery_task_id']),
        ]
        ordering = ['-started_at']
        
    def __str__(self):
        return f"{self.schedule} - {self.status} ({self.started_at})"
        
    def save(self, *args, **kwargs):
        if self.completed_at and self.started_at:
            self.execution_time = self.completed_at - self.started_at
        super().save(*args, **kwargs)
        
    @property
    def duration_seconds(self):
        if self.execution_time:
            return self.execution_time.total_seconds()
        return None
        
    @property
    def is_completed(self):
        return self.status in ['success', 'failure']