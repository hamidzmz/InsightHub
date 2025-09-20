from django.core.exceptions import ValidationError


def validate_user_schedule_limit(user, exclude_pk=None):
    from .models import Schedule
    
    if not user.is_superuser:
        query = Schedule.objects.filter(user=user, is_active=True)
        if exclude_pk:
            query = query.exclude(pk=exclude_pk)
        if query.count() >= 5:
            raise ValidationError("Regular users cannot have more than 5 active jobs")


def validate_cron_expression(value):
    from croniter import croniter
    if not croniter.is_valid(value):
        raise ValidationError("Invalid cron expression format")


def validate_task_parameters(parameters, task_definition):
    errors = task_definition.validate_parameters(parameters)
    if errors:
        error_messages = []
        for field, message in errors.items():
            error_messages.append(message)
        raise ValidationError(error_messages)