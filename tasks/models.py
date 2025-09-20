from django.db import models
from core.models import BaseModel


class TaskDefinition(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    celery_task_name = models.CharField(max_length=200, unique=True)
    input_schema = models.JSONField(default=dict)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'task_definitions'
        indexes = [
            models.Index(fields=['is_active']),
            models.Index(fields=['celery_task_name']),
        ]
        ordering = ['name']
        
    def __str__(self):
        return self.name
        
    @property
    def input_fields(self):
        return list(self.input_schema.keys())
        
    def validate_parameters(self, parameters):
        errors = {}
        
        for field_name, field_type in self.input_schema.items():
            if field_name in parameters:
                value = parameters[field_name]
                
                if field_type == 'string' and not isinstance(value, str):
                    errors[field_name] = f"{field_name} must be a string"
                elif field_type == 'integer' and not isinstance(value, int):
                    errors[field_name] = f"{field_name} must be an integer"
                elif field_type == 'boolean' and not isinstance(value, bool):
                    errors[field_name] = f"{field_name} must be a boolean"
                elif field_type == 'float' and not isinstance(value, (int, float)):
                    errors[field_name] = f"{field_name} must be a number"
        
        return errors