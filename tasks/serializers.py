from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field
from .models import TaskDefinition


class TaskDefinitionSerializer(serializers.ModelSerializer):
    input_fields = serializers.SerializerMethodField()
    
    class Meta:
        model = TaskDefinition
        fields = ['id', 'name', 'description', 'input_schema', 'input_fields', 'is_active', 'created_at']
        read_only_fields = ['id', 'created_at']
    
    @extend_schema_field(serializers.ListField(child=serializers.CharField()))
    def get_input_fields(self, obj) -> list:
        return obj.input_fields