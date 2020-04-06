from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand

from security.models import User
import string
import secrets

class Command(BaseCommand):
    args = ''
    help = 'Creates an admin user if no other users exist'

    def handle(self, *args, **options):
        adminCount = User.objects.filter(deleted=False).filter(is_superuser=True).count()
        if adminCount > 0:
            print("Admin user(s) already exist, not creating a new one")
            return
        print("--------------------------------------------------------------------")
        print("There are no valid admin users, creating one")
        password = ''.join(secrets.choice(string.ascii_letters + string.digits) for i in range(16))
        existing = User.objects.filter(email="admin@admin")
        if existing.count() == 0: 
            user = User.objects.create_user(email="admin@admin", password=password, is_superuser=True, receivesAlerts=False)
        else:
            user = existing
            user.deleted = False
            user.password = password
            user.receivesAlerts = False
            user.is_superuser = True
        user.save()
        print("Admin Username: admin@admin")
        print("Admin password: " + password)
        print("--------------------------------------------------------------------")

