from background_task.models import Task
from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand

from itemManagement.models import Location, Item, Photo, ItemStorage, Tag
from logs.models import UserLogs, LOGCODE_000000, LOGMSG_000000
from security.models import User
import base64


class Command(BaseCommand):
    args = ''
    help = 'Creates and listens for background tasks'


    def handle(self, *args, **options):
        from logs.tasks import removeExpiredLogs
        Task.objects.filter(verbose_name="removeExpiredLogs").delete()  # Delete the task if there is already one running
        removeExpiredLogs(verbose_name="removeExpiredLogs", repeat=604800) # One week 604800
        call_command('process_tasks')  # Listens for background tasks. Note that this is a blocking call and will not stop without being cancelled

