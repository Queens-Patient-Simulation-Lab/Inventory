from django.urls import reverse

from itemManagement.models import Location
from simulation_lab.BaseTestCaseView import BaseTestCaseView
from simulation_lab.TestUtils import createLoggedInUser


class GetLocationViewTestsAccessible(BaseTestCaseView):

    def test_notLoggedIn_cannotAccess(self):
        response = self.client.get("/item/locations/")
        self.assertEqual(response.status_code, 302)

    def test_loggedInAsLabAssistant_cannotAccess(self):
        pass  # TODO, test that only admin can request these views.

    def test_loggedInAsAdmin_canGetLocations(self):
        createLoggedInUser(self, isAdmin=True)

        response = self.client.get("/item/locations/")
        self.assertEqual(response.status_code, 200)


class GetLocationViewTestsLoggedIn(BaseTestCaseView):

    def setUp(self):
        createLoggedInUser(self, isAdmin=True)

    def test_multipleLocationsExist_contextHasLocations(self):
        Location.objects.create(name="TestLocationOne")
        Location.objects.create(name="TestLocationTwo")

        response = self.client.get(reverse('location-list'))
        locationQuery = response.context['locations']
        self.assertEqual(locationQuery.count(), 2)
        self.assertTrue(locationQuery.filter(name="TestLocationOne").exists())
        self.assertTrue(locationQuery.filter(name="TestLocationTwo").exists())

    def test_locationDeleted_contextDoesNotHaveLocation(self):
        Location.objects.create(name="TestLocation", deleted=True)
        response = self.client.get(reverse('location-list'))
        self.assertEqual(response.context['locations'].count(), 0)


class PostLocationViewTests(BaseTestCaseView):
    def setUp(self):
        createLoggedInUser(self, isAdmin=True)
    def makeCall(self, data):
        return self.client.post(reverse('location-list'), data=data)
    def test_addLocation_happyPath_givesSuccessMessage(self):
        Location.objects.create(name="TestLocationOne")
        data = {
            'name': "TEST",
            "description": " TestDescription"
        }
        response = self.makeCall(data)
        self.assertMessageLevel(response, self.MESSAGE_SUCCESS)

    def test_addLocation_happyPath_contextHasLocation(self):
        data = {
            'name': "TEST",
            "description": " TestDescription"
        }
        response = self.makeCall(data)
        locations = response.context['locations']
        self.assertEqual(len(locations), 1)
        first = locations.first()
        self.assertEqual("TEST", first.name)
        self.assertEqual("TestDescription", first.description)

    def test_addLocation_emptyName_failsWithMessage(self):
        data = {
            'name': "",
            "description": " TestDescription"
        }
        response = self.makeCall(data)
        locations = response.context['locations']
        self.assertEqual(len(locations), 0)
        self.assertMessageLevel(response, self.MESSAGE_ERROR)

    def test_addLocation_givenNameWithSpacesOnEnds_stripsSpaces(self):
        data = {
            'name': "  TEST NAME  ",
            "description": " TestDescription"
        }
        response = self.makeCall(data)
        locations = response.context['locations']
        self.assertEqual(len(locations), 1)
        first = locations.first()
        self.assertNotEqual( "  TEST NAME  ", first.name)
        self.assertEqual( "TEST NAME", first.name)
        self.assertEqual("TestDescription", first.description)

    def test_addLocation_shortName_failsWithMessage(self):
        pass

    def test_addLocation_duplicateActiveLocations_failsWithMessage(self):
        pass

    def test_addLocation_duplicateInactiveLocations_succeedsWithMessage(self):
        pass

    def test_updateLocation_idDoesntExist_failsWithMessage(self):
        pass

    def test_updateLocation_happyPath_showsMessage(self):
        pass

    def test_idProvidedHappyPath_editsLocation(self):
        pass


class DeleteLocationViewTests(BaseTestCaseView):
    def setUp(self):
        createLoggedInUser(self, isAdmin=True)

    def test_happyPath_onlySoftDeletesLocation(self):
        pass
