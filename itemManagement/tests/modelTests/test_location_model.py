from django.test import SimpleTestCase, TestCase

from itemManagement.models import Location, Item, ItemStorage


class LocationModelTests(TestCase):
    def setUp(self):
        pass

    def test_getLocationDetailsForItem_returnsCorrectDetails(self):
        sut = Location.objects.create(name="TestName", description="TestDescription")
        item = Item.objects.create(title="TestTitle")
        ItemStorage.objects.create(item=item, location=sut, quantity=15)

        result = sut.getLocationDetailsForItem(item)
        self.assertEqual(result['name'], "TestName")
        self.assertEqual(result['description'], "TestDescription")
        self.assertEqual(result['quantity'], 15)
    def test_getLocationDetailsForItem_ItemHasMultipleLocations_onlyConsidersQuantityForLocation(self):
        sut = Location.objects.create(name="TestName")
        differentLocation = Location.objects.create(name="different")

        item = Item.objects.create(title="TestTitle")
        ItemStorage.objects.create(item=item, location=sut, quantity=15)
        ItemStorage.objects.create(item=item, location=differentLocation, quantity=20)

        result = sut.getLocationDetailsForItem(item)

        self.assertEqual(result['quantity'], 15)

    def test_getLocationDetailsForItem_doesNotGiveDeletedField(self):
        sut = Location.objects.create(name="TestName", description="TestDescription")
        item = Item.objects.create(title="TestTitle")
        ItemStorage.objects.create(item=item, location=sut, quantity=20)

        assert "name" in sut.getLocationDetailsForItem(item)
        assert "deleted" not in sut.getLocationDetailsForItem(item)


