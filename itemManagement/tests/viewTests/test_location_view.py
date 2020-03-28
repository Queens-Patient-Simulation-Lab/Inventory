from django.urls import reverse

from itemManagement.models import Location, Item, ItemStorage
from itemManagement.urls import URL_LOCATION_LIST
from simulation_lab.BaseTestCaseView import BaseTestCaseView


class GetLocationViewTestsAccessible(BaseTestCaseView):

    def test_notLoggedIn_cannotAccess(self):
        response = self.client.get("/item/locations/")
        self.assertEqual(response.status_code, 302)

    def test_loggedInAsLabAssistant_cannotAccess(self):
        self.createLoggedInUser(isAdmin=False)

        response = self.client.get("/item/locations/")
        self.assertEqual(response.status_code, 403)

    def test_loggedInAsAdmin_canGetLocations(self):
        self.createLoggedInUser(isAdmin=True)

        response = self.client.get("/item/locations/")
        self.assertEqual(response.status_code, 200)


class GetLocationViewTestsLoggedIn(BaseTestCaseView):

    def setUp(self):
        self.createLoggedInUser(isAdmin=True)

    def test_multipleLocationsExist_contextHasLocations(self):
        Location.objects.create(name="TestLocationOne")
        Location.objects.create(name="TestLocationTwo")

        response = self.client.get(reverse(URL_LOCATION_LIST))
        locationQuery = response.context['locations']
        self.assertEqual(locationQuery.count(), 2)
        self.assertTrue(locationQuery.filter(name="TestLocationOne").exists())
        self.assertTrue(locationQuery.filter(name="TestLocationTwo").exists())

    def test_locationDeleted_contextDoesNotHaveLocation(self):
        Location.objects.create(name="TestLocation", deleted=True)
        response = self.client.get(reverse(URL_LOCATION_LIST))
        self.assertEqual(response.context['locations'].count(), 0)


class PostLocationViewTests(BaseTestCaseView):
    def setUp(self):
        self.createLoggedInUser(isAdmin=True)

    def makeCall(self, data):
        return self.client.post(reverse(URL_LOCATION_LIST), data=data, follow=True)

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

    def test_addLocation_happyPath_redirects(self):
        Location.objects.create(name="TestLocationOne")
        data = {
            'name': "TEST",
            "description": " TestDescription"
        }
        response = self.makeCall(data)
        self.assertRedirects(response, reverse(URL_LOCATION_LIST))
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
        self.assertNotEqual("  TEST NAME  ", first.name)
        self.assertEqual("TEST NAME", first.name)
        self.assertEqual("TestDescription", first.description)

    def test_addLocation_shortName_failsWithMessage(self):
        data = {
            'name': "ab",
            "description": " TestDescription"
        }
        response = self.makeCall(data)
        locations = response.context['locations']
        self.assertEqual(len(locations), 0)
        self.assertMessageLevel(response, self.MESSAGE_ERROR)

    def test_addLocation_duplicateActiveLocations_failsWithMessage(self):
        Location.objects.create(name="abc")
        self.assertEqual(Location.objects.count(), 1)

        data = {
            'name': "abc",
            "description": " TestDescription"
        }
        response = self.makeCall(data)
        locations = response.context['locations']
        self.assertEqual(len(locations), 1)
        self.assertMessageLevel(response, self.MESSAGE_ERROR)

    def test_addLocation_duplicateInactiveLocations_succeedsWithMessage(self):
        Location.objects.create(name="one")
        self.assertEqual(Location.objects.count(), 1)

        data = {
            'name': "another",
            "description": " TestDescription"
        }
        response = self.makeCall(data)
        locations = response.context['locations']
        self.assertEqual(len(locations), 2)
        self.assertMessageLevel(response, self.MESSAGE_SUCCESS)

    def test_updateLocation_idDoesntExist_failsWithMessage(self):
        Location.objects.create(id=11, name="one")
        self.assertEqual(Location.objects.count(), 1)

        data = {
            'id': 22,
            'name': "another",
            "description": " TestDescription"
        }
        response = self.makeCall(data)
        locations = response.context['locations']
        self.assertEqual(len(locations), 1)
        self.assertMessageLevel(response, self.MESSAGE_ERROR)

    def test_updateLocation_happyPath_showsMessage(self):
        Location.objects.create(id=11, name="one")
        self.assertEqual(Location.objects.count(), 1)

        data = {
            'id': 11,
            'name': "another",
            "description": " TestDescription"
        }
        response = self.makeCall(data)
        locations = response.context['locations']
        self.assertEqual(len(locations), 1)
        self.assertMessageLevel(response, self.MESSAGE_SUCCESS)

    def test_idProvidedHappyPath_editsLocation(self):
        Location.objects.create(id=11, name="one")
        self.assertEqual(Location.objects.count(), 1)

        data = {
            'id': 11,
            'name': "another",
            "description": "TestDescription"
        }
        response = self.makeCall(data)
        locations = response.context['locations']
        self.assertEqual(len(locations), 1)
        location = locations.first()
        self.assertEqual(location.id, data['id'])
        self.assertEqual(location.name, data['name'])
        self.assertEqual(location.description, data['description'])


class DeleteLocationViewTests(BaseTestCaseView):
    def setUp(self):
        self.createLoggedInUser(isAdmin=True)

    def test_happyPath_onlySoftDeletesLocation(self):
        Location.objects.create(id=11, name="one")
        self.assertEqual(Location.objects.count(), 1)

        self.client.delete(reverse("location-list", args=(11,)))
        self.assertEqual(Location.objects.count(), 1, "Hard delete occurred")
        location = Location.objects.get(id=11)
        self.assertEqual(location.deleted, True, "Soft delete didn't occur")

    def test_deleteFails_givesErrorCode400(self):
        testLocation = Location.objects.create(id=11, name="testLocation")
        item = Item.objects.create(title="TestItem")
        storage = ItemStorage.objects.create(item=item, location=testLocation, quantity=13)

        response = self.client.delete(reverse("location-list", args=(11,)))
        self.assertEqual(response.status_code, 400)

    def test_locationHasRelatedItems_cantDelete(self):
        testLocation = Location.objects.create(id=11,name="testLocation")
        item = Item.objects.create(title="TestItem")
        storage = ItemStorage.objects.create(item=item, location=testLocation, quantity=13)

        response = self.client.delete(reverse("location-list", args=(11,)))
        self.assertEqual(response.status_code, 400)
        response = self.client.get(reverse("location-list"))

        self.assertEqual(response.context['locations'].count(), 1)
        self.assertMessageLevel(response, self.MESSAGE_ERROR)

    def test_locationHasRelatedItemsOfNoQuantity_canDelete(self):
        testLocation = Location.objects.create(id=11,name="testLocation")
        item = Item.objects.create(title="TestItem")
        storage = ItemStorage.objects.create(item=item, location=testLocation, quantity=0)

        response = self.client.delete(reverse("location-list", args=(11,)))
        self.assertEqual(response.status_code, 204)
        response = self.client.get(reverse("location-list"))

        self.assertEqual(response.context['locations'].count(), 0)
        self.assertMessageLevel(response, self.MESSAGE_SUCCESS)
