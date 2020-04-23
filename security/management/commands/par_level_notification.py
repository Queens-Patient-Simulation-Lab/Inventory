from django.core.management.base import BaseCommand
from security.models import User
from itemManagement.models import Item
from emails.email import EmailManager as em


class Command(BaseCommand):
    args = ''
    help = 'send weekly notification email'

    def handle(self, *args, **options):
        items = list(filter(lambda x: x.needToNotifyAdmin, Item.objects.filter(deleted=False)))
        em.sendAlertEmails(items)
