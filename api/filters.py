from rest_framework.filters import BaseFilterBackend
import django_filters


class DynamicFilterBackend(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        if request.method == 'POST' and hasattr(request, 'data'):
            filters = request.data.get('filters', {})
            ordering = request.data.get('ordering', [])
            
            for field, value in filters.items():
                if hasattr(queryset.model, field):
                    queryset = queryset.filter(**{field: value})
            
            if ordering:
                valid_fields = [f.name for f in queryset.model._meta.fields]
                safe_ordering = [o for o in ordering if o.lstrip('-') in valid_fields]
                if safe_ordering:
                    queryset = queryset.order_by(*safe_ordering)
        
        return queryset


class ScheduleFilter(django_filters.FilterSet):
    user = django_filters.NumberFilter()
    task_definition = django_filters.NumberFilter()
    is_active = django_filters.BooleanFilter()
    created_at = django_filters.DateTimeFromToRangeFilter()
    
    class Meta:
        from schedules.models import Schedule
        model = Schedule
        fields = ['user', 'task_definition', 'is_active', 'created_at']


class ExecutionLogFilter(django_filters.FilterSet):
    schedule = django_filters.NumberFilter()
    status = django_filters.ChoiceFilter(choices=[
        ('pending', 'Pending'),
        ('running', 'Running'),
        ('success', 'Success'),
        ('failure', 'Failure'),
        ('retry', 'Retry'),
    ])
    started_at = django_filters.DateTimeFromToRangeFilter()
    
    class Meta:
        from executions.models import ExecutionLog
        model = ExecutionLog
        fields = ['schedule', 'status', 'started_at']