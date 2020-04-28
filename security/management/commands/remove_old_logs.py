from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from logs.models import Log


class Command(BaseCommand):
    args = ''
    help = 'Remove all logs older than a year'


    def handle(self, *args, **options):
        expiryDate = timezone.now() - timedelta(days=365)
        Log.objects.filter(time__lt=expiryDate).delete()
