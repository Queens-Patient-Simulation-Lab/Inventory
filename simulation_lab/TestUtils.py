from django.test import TestCase

from security.models import User



def createLoggedInUser(testCase, isAdmin):
    #FIXME: Implement logic for admin

    testCase.client.force_login(User.objects.create_user("test@a.com", "test"))

