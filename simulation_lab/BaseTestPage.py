from django.test import TestCase

from security.models import User


class BaseTestPage(TestCase):

    def createLoggedInUser(self, isAdmin):
        #FIXME: Implement logic for admin

        self.client.force_login(User.objects.create_user("test@a.com", "test"))

