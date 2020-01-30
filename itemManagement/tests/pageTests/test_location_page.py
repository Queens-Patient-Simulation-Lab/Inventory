from django.test import TestCase, Client
from django.urls import reverse
from django.contrib import auth

from security.models import User
from simulation_lab.BaseTestPage import BaseTestPage


class LocationPageTests(BaseTestPage):

    # TODO, test that only admin can request these views.

    def test_notLoggedIn_cannotAccess(self):
        response = self.client.get("/item/locations/")
        self.assertEqual(response.status_code, 302)

    def test_loggedInAsLabAssistant_cannotAccess(self):
        pass  # todo

    def test_loggedInAsAdmin_canGetLocations(self):
        self.createLoggedInUser(isAdmin=True)

        response = self.client.get("/item/locations/")
        self.assertEqual(response.status_code, 200)

    def test_onClick_addLocation_showsModal(self):
        pass
    def test_onClick_addLocationAgain_showsEmptyModal(self):
        pass
    def test_onAddLocation_happyPath_showsSuccessMessage(self):
        pass
    def test_onAddLocation_duplicateName_showsErrorMessage(self):
        pass
    def test_onAddLocationSubmition_makesPostRequest(self):
        pass
    def test_onClick_delete_showsSuccessMessage(self):
        pass
    def test_onClick_edit_showsEditModal(self):
        pass
    def test_onShowEditModal_hasCorrectDetails(self):
        pass
    # Tests that the details updates when you change the location you are editing
    def test_onShowDifferentEditModal_hasCorrectDetails(self):
        pass
    def test_onEditModalSuccess_showsSuccessMessage(self):
        pass
    def test_onEditModalSubmition_makesPostRequest(self):
        pass


