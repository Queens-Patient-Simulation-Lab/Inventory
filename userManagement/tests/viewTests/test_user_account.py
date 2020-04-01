from security.models import User
from simulation_lab.BaseTestCaseView import BaseTestCaseView


class GetUserAccountViewTestsAccessible(BaseTestCaseView):

    def test_notLoggedIn_cannotAccess(self):
        response = self.client.get("/userManagement/user_account/")
        self.assertEqual(response.status_code, 302)

    def test_loggedInAsAdmin_canGetUserAccount(self):
        self.createLoggedInUser(isAdmin=True)

        response = self.client.get("/userManagement/user_account/")
        self.assertEqual(response.status_code, 200)


class GetUserAccountViewTestsLoggedIn(BaseTestCaseView):

    def setUp(self):
        self.createLoggedInUser(isAdmin=True)

    def test_multipleUserExist_contextHasAllUsers(self):
        User.objects.create_user("test1@test.com", "Test1234")
        User.objects.create_user("test2@test.com", "Test1234")

        response = self.client.get("/userManagement/user_account/")
        staffQuery = response.context['staff']
        self.assertEqual(staffQuery.count(), 3)
        self.assertEqual(staffQuery.filter(email="test1@test.com").count(), 1)
        self.assertEqual(staffQuery.filter(email="test2@test.com").count(), 1)
        self.assertEqual(staffQuery.filter(email="test@test.com").count(), 1)

    def test_userDeleted_contextHasNoDeletedUsers(self):
        User.objects.create_user("test1@test.com", "test1234", deleteFlag=True)

        response = self.client.get("/userManagement/user_account/")
        staffQuery = response.context['staff']
        self.assertEqual(staffQuery.count(), 1)
        self.assertEqual(staffQuery.filter(deleteFlag=False).count(), 1)
        self.assertEqual(staffQuery.filter(deleteFlag=True).count(), 0)


class PostUserAccountViewTests(BaseTestCaseView):
    def setUp(self):
        self.createLoggedInUser(isAdmin=True)

    def test_emailInvitation_emailSent(self):
        #TODO email Invitation
        pass



#TODO class actionViewUserAccountViewTests(BaseTestCaseView):
