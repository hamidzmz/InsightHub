from celery import shared_task
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
import time
import random
import json


@shared_task(bind=True)
def send_email_task(self, schedule_id, parameters):
    from schedules.models import Schedule
    from executions.models import ExecutionLog
    
    try:
        schedule = Schedule.objects.select_related('user', 'task_definition').get(id=schedule_id)
    except Schedule.DoesNotExist:
        return {'error': 'Schedule not found'}
    
    execution_log = ExecutionLog.objects.create(
        schedule=schedule,
        celery_task_id=self.request.id,
        status='running',
        started_at=timezone.now()
    )
    
    try:
        email = parameters.get('email')
        delay = parameters.get('delay', 0)
        
        if delay:
            time.sleep(delay)
        
        send_mail(
            subject=f'Scheduled Email from {schedule.user.username}',
            message=f'This is a scheduled email task executed at {timezone.now()}.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
        )
        
        execution_log.status = 'success'
        execution_log.result = {'email_sent': True, 'recipient': email}
        execution_log.completed_at = timezone.now()
        execution_log.execution_time = timezone.now() - execution_log.started_at
        execution_log.save()
        
        return execution_log.result
        
    except Exception as exc:
        execution_log.status = 'failure'
        execution_log.error_message = str(exc)
        execution_log.completed_at = timezone.now()
        execution_log.execution_time = timezone.now() - execution_log.started_at
        execution_log.save()
        
        raise self.retry(exc=exc, countdown=60, max_retries=3)


@shared_task(bind=True)
def data_processing_task(self, schedule_id, parameters):
    from schedules.models import Schedule
    from executions.models import ExecutionLog
    
    try:
        schedule = Schedule.objects.get(id=schedule_id)
    except Schedule.DoesNotExist:
        return {'error': 'Schedule not found'}
    
    execution_log = ExecutionLog.objects.create(
        schedule=schedule,
        celery_task_id=self.request.id,
        status='running',
        started_at=timezone.now()
    )
    
    try:
        dataset_size = parameters.get('dataset_size', 1000)
        processing_type = parameters.get('processing_type', 'simple')
        
        time.sleep(2)
        
        if processing_type == 'complex':
            time.sleep(3)
            result = {
                'processed_records': dataset_size,
                'processing_type': processing_type,
                'statistics': {
                    'mean': random.uniform(10, 100),
                    'median': random.uniform(10, 100),
                    'std_dev': random.uniform(1, 10)
                }
            }
        else:
            result = {
                'processed_records': dataset_size,
                'processing_type': processing_type,
                'total_time': '2 seconds'
            }
        
        execution_log.status = 'success'
        execution_log.result = result
        execution_log.completed_at = timezone.now()
        execution_log.execution_time = timezone.now() - execution_log.started_at
        execution_log.save()
        
        return result
        
    except Exception as exc:
        execution_log.status = 'failure'
        execution_log.error_message = str(exc)
        execution_log.completed_at = timezone.now()
        execution_log.execution_time = timezone.now() - execution_log.started_at
        execution_log.save()
        
        raise self.retry(exc=exc, countdown=120, max_retries=2)


@shared_task(bind=True)
def generate_report_task(self, schedule_id, parameters):
    from schedules.models import Schedule
    from executions.models import ExecutionLog
    
    try:
        schedule = Schedule.objects.get(id=schedule_id)
    except Schedule.DoesNotExist:
        return {'error': 'Schedule not found'}
    
    execution_log = ExecutionLog.objects.create(
        schedule=schedule,
        celery_task_id=self.request.id,
        status='running',
        started_at=timezone.now()
    )
    
    try:
        report_type = parameters.get('report_type', 'basic')
        include_charts = parameters.get('include_charts', False)
        
        time.sleep(1)
        
        result = {
            'report_type': report_type,
            'include_charts': include_charts,
            'generated_at': timezone.now().isoformat(),
            'file_size': f"{random.randint(100, 1000)}KB",
            'pages': random.randint(5, 50)
        }
        
        if include_charts:
            result['charts_generated'] = random.randint(3, 10)
        
        execution_log.status = 'success'
        execution_log.result = result
        execution_log.completed_at = timezone.now()
        execution_log.execution_time = timezone.now() - execution_log.started_at
        execution_log.save()
        
        return result
        
    except Exception as exc:
        execution_log.status = 'failure'
        execution_log.error_message = str(exc)
        execution_log.completed_at = timezone.now()
        execution_log.execution_time = timezone.now() - execution_log.started_at
        execution_log.save()
        
        raise self.retry(exc=exc, countdown=90, max_retries=2)


@shared_task(bind=True)
def file_backup_task(self, schedule_id, parameters):
    from schedules.models import Schedule
    from executions.models import ExecutionLog
    
    try:
        schedule = Schedule.objects.get(id=schedule_id)
    except Schedule.DoesNotExist:
        return {'error': 'Schedule not found'}
    
    execution_log = ExecutionLog.objects.create(
        schedule=schedule,
        celery_task_id=self.request.id,
        status='running',
        started_at=timezone.now()
    )
    
    try:
        source_path = parameters.get('source_path', '/tmp')
        destination = parameters.get('destination', '/backup')
        compress = parameters.get('compress', False)
        
        time.sleep(3)
        
        result = {
            'source_path': source_path,
            'destination': destination,
            'compressed': compress,
            'files_backed_up': random.randint(10, 100),
            'total_size': f"{random.randint(1, 100)}MB"
        }
        
        execution_log.status = 'success'
        execution_log.result = result
        execution_log.completed_at = timezone.now()
        execution_log.execution_time = timezone.now() - execution_log.started_at
        execution_log.save()
        
        return result
        
    except Exception as exc:
        execution_log.status = 'failure'
        execution_log.error_message = str(exc)
        execution_log.completed_at = timezone.now()
        execution_log.execution_time = timezone.now() - execution_log.started_at
        execution_log.save()
        
        raise self.retry(exc=exc, countdown=180, max_retries=1)


@shared_task(bind=True)
def database_cleanup_task(self, schedule_id, parameters):
    from schedules.models import Schedule
    from executions.models import ExecutionLog
    
    try:
        schedule = Schedule.objects.get(id=schedule_id)
    except Schedule.DoesNotExist:
        return {'error': 'Schedule not found'}
    
    execution_log = ExecutionLog.objects.create(
        schedule=schedule,
        celery_task_id=self.request.id,
        status='running',
        started_at=timezone.now()
    )
    
    try:
        days_old = parameters.get('days_old', 30)
        table_name = parameters.get('table_name', 'logs')
        
        time.sleep(2)
        
        result = {
            'table_name': table_name,
            'days_old': days_old,
            'records_deleted': random.randint(5, 50),
            'space_freed': f"{random.randint(1, 20)}MB"
        }
        
        execution_log.status = 'success'
        execution_log.result = result
        execution_log.completed_at = timezone.now()
        execution_log.execution_time = timezone.now() - execution_log.started_at
        execution_log.save()
        
        return result
        
    except Exception as exc:
        execution_log.status = 'failure'
        execution_log.error_message = str(exc)
        execution_log.completed_at = timezone.now()
        execution_log.execution_time = timezone.now() - execution_log.started_at
        execution_log.save()
        
        raise self.retry(exc=exc, countdown=120, max_retries=2)