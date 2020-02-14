from security.models import User
from simulation_lab.BaseTestCaseView import BaseTestCaseView


class GetUserAccountViewTestsAccessible(BaseTestCaseView):

    def test_notLoggedIn_cannotAccess(self):
        response = self.client.get("/userManagement/user_account/")
        self.assertEqual(response.status_code, 302)

    def test_loggedInAsLabAssistant_cannotAccess(self):
        self.createLoggedInUser(isAdmin=False)

        response = self.client.get("/userManagement/user_account/")
        self.assertEqual(response.status_code, 403)

    def test_loggedInAsAdmin_canGetLocations(self):
        self.createLoggedInUser(isAdmin=True)

        response = self.client.get("/userManagement/user_account/")
        self.assertEqual(response.status_code, 200)


class GetUserAccountViewTestsLoggedIn(BaseTestCaseView):

    def setUp(self):
        self.createLoggedInUser(isAdmin=True)

    def test_multipleUserExist_contextHasUsers(self):
        User.objects.create_user("test1@test.com", "test1234")
        User.objects.create_user("test2@test.com", "test1234")

        response = self.client.get("/userManagement/user_account/")
        staffQuery = response.context['staff']
        self.assertEqual(staffQuery.count(), 3)
        self.assertTrue(staffQuery.filter(name="test1@test.com").exists())
        self.assertTrue(staffQuery.filter(name="test2@test.com").exists())
        self.assertTrue(staffQuery.filter(name="test@test.com").exists())

    def test_locationDeleted_contextDoesNotHaveLocation(self):
        User.objects.create_user("test1@test.com", "test1234", deleteFlag=True)

        response = self.client.get("/userManagement/user_account/")
        staffQuery = response.context['staff']
        self.assertEqual(staffQuery.count(), 2)
        self.assertEqual(staffQuery.filter(deleteFlag=False).count(), 1)
        self.assertEqual(staffQuery.filter(deleteFlag=True).count(), 1)


class PostUserAccountViewTests(BaseTestCaseView):
    def setUp(self):
        self.createLoggedInUser(isAdmin=True)

    def test_emailInvitation_emailSent(self):
        #TODO email Invitation
        pass



#TODO class actionViewUserAccountViewTests(BaseTestCaseView):
