from django.test import TestCase, client

from security.models import User


class BaseTestCaseView(TestCase):
    MESSAGE_SUCCESS = "success"
    MESSAGE_ERROR = "danger"

    def assertMessageLevel(self, response, messageLevel):
        assert messageLevel in [x.tags for x in response.context['messages']],f"{messageLevel} banner was not provided"

    def createLoggedInUser(self, isAdmin):
        # TODO: Implement logic for admin

        self.client.force_login(User.objects.create_user("test@a.com", "test"))
