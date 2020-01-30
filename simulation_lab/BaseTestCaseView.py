from django.test import TestCase


class BaseTestCaseView(TestCase):
    MESSAGE_SUCCESS = "success"
    MESSAGE_ERROR = "danger"

    def assertMessageLevel(self, response, messageLevel):
        assert messageLevel in [x.tags for x in response.context['messages']]
