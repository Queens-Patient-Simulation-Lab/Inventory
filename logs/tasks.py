from datetime import timedelta, datetime

from background_task import background
from django.contrib.auth.models import User

# https://django-background-tasks.readthedocs.io/en/latest/
from django.utils import timezone

from itemManagement.models import Item
from logs.models import UserLogs, ItemCountLogs, ItemInfoLogs


@background(schedule=1)
def removeExpiredLogs():
    expiryDate = timezone.now() - timedelta(days=365)

    UserLogs.objects.filter(time__lt=expiryDate).delete()
    ItemCountLogs.objects.filter(time__lt=expiryDate).delete()
    ItemInfoLogs.objects.filter(time__lt=expiryDate).delete()
