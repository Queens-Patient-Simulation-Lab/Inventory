from django.test import TestCase

from simulation_lab.TestUtils import createLoggedInUser


class LocationPageTests(TestCase):

    def setUp(self):
        createLoggedInUser(self, isAdmin=True)
    def test_onClick_addLocation_showsModal(self):
        pass
    def test_onClick_addLocationAgain_showsEmptyModal(self):
        pass
    def test_onAddLocationSubmition_makesPostRequest(self):
        pass
    def test_onClick_edit_showsEditModal(self):
        pass
    def test_onShowEditModal_hasCorrectDetails(self):
        pass
    # Tests that the details updates when you change the location you are editing
    def test_onShowDifferentEditModal_hasCorrectDetails(self):
        pass
    def test_onEditModalSubmition_makesPostRequest(self):
        pass


