from django.core.management.base import BaseCommand
from tasks.models import TaskDefinition


class Command(BaseCommand):
    help = 'Seed the database with predefined task definitions'
    
    def handle(self, *args, **options):
        tasks = [
            {
                'name': 'Send Email',
                'description': 'Send an email with optional delay',
                'celery_task_name': 'tasks.celery_tasks.send_email_task',
                'input_schema': {
                    'email': 'string',
                    'delay': 'integer'
                }
            },
            {
                'name': 'Data Processing',
                'description': 'Process dataset with specified parameters',
                'celery_task_name': 'tasks.celery_tasks.data_processing_task',
                'input_schema': {
                    'dataset_size': 'integer',
                    'processing_type': 'string'
                }
            },
            {
                'name': 'Report Generation',
                'description': 'Generate reports with custom format',
                'celery_task_name': 'tasks.celery_tasks.generate_report_task',
                'input_schema': {
                    'report_type': 'string',
                    'include_charts': 'boolean'
                }
            },
            {
                'name': 'File Backup',
                'description': 'Backup files to specified location',
                'celery_task_name': 'tasks.celery_tasks.file_backup_task',
                'input_schema': {
                    'source_path': 'string',
                    'destination': 'string',
                    'compress': 'boolean'
                }
            },
            {
                'name': 'Database Cleanup',
                'description': 'Clean up old database records',
                'celery_task_name': 'tasks.celery_tasks.database_cleanup_task',
                'input_schema': {
                    'days_old': 'integer',
                    'table_name': 'string'
                }
            }
        ]
        
        created_count = 0
        for task_data in tasks:
            task_definition, created = TaskDefinition.objects.get_or_create(
                name=task_data['name'],
                defaults=task_data
            )
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Created task: {task_definition.name}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Task already exists: {task_definition.name}')
                )
        
        self.stdout.write(
            self.style.SUCCESS(f'Seeding completed. Created {created_count} new tasks.')
        )