from django.test import TestCase, client

from security.models import User


class BaseTestCaseView(TestCase):
    MESSAGE_SUCCESS = "success"
    MESSAGE_ERROR = "danger"

    def assertMessageLevel(self, response, messageLevel):
        assert messageLevel in [x.tags for x in response.context['messages']],f"{messageLevel} banner was not provided"

    def createLoggedInUser(self, isAdmin):
        if isAdmin:
            User.objects.create_user(email="test@test.com", password="Test1234", is_superuser=True)
        else:
            User.objects.create_user("test@test.com", "Test1234")
        self.client.login(email="test@test.com", password="Test1234")
