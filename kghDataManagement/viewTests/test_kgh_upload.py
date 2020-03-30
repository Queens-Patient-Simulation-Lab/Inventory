import csv
import io
from decimal import Decimal

from django.urls import reverse

from itemManagement.models import Item
from kghDataManagement.urls import URL_KGH_UPLOAD_PAGE
from simulation_lab.BaseTestCaseView import BaseTestCaseView


class PostKghSpreadsheet(BaseTestCaseView):

    def makeCallWithCSV(self, itemList, addHeader=True, fileName="kghFile.csv"):
        content = ""
        if addHeader:
            content += "Material,Material Description,Un,Old material no.,,,Matl grp,Basic material,Type,MA price,\r\n"
        for row in itemList:
            content += ",".join(row)
            content += ('\r\n')

        self.inMemoryBuffer = io.StringIO(content)
        self.inMemoryBuffer.name = fileName
        data = {
            'kghFile': self.inMemoryBuffer
        }
        return self.client.post(reverse(URL_KGH_UPLOAD_PAGE), data=data, follow=True)

    def createCsvRowData(
            self,
            material="",
            materialDescription="",
            un="",
            oldMaterialNumbers="",
            matlGrp="",
            basicMaterial="",
            type="",
            maPrice="",
            currency=""
    ):
        return [material, materialDescription, un, oldMaterialNumbers, "", "", matlGrp, basicMaterial, type, maPrice,
                currency]

    def setUp(self):
        self.createLoggedInUser(isAdmin=True)

        self.inMemoryBuffer = io.StringIO()
        self.inMemoryBuffer.name = "Test.csv"

    def tearDown(self):
        self.inMemoryBuffer.close()

    def test_fileNotProvided_givesError(self):
        response = self.client.post(reverse(URL_KGH_UPLOAD_PAGE), follow=True)
        self.assertMessageLevel(response, self.MESSAGE_ERROR)



    def test_kghItemsNotInDatabase_doesNothingAndSucceeds(self):
        itemOne = Item.objects.create(
            title="Item One",
            price=3,
            kghID=11
        )

        itemList = [
            self.createCsvRowData(material="999999", maPrice="11.50", materialDescription="somethingDifferent"),
        ]
        response = self.makeCallWithCSV(itemList)

        self.assertMessageLevel(response, self.MESSAGE_SUCCESS)

        itemOne.refresh_from_db()

        self.assertEqual(itemOne.kghID, "11")
        self.assertEqual(itemOne.price, Decimal("3"))
        self.assertEqual(itemOne.title, "Item One")

    def test_kghItemsSoftDeleted_doesNothingAndSucceeds(self):
        itemOne = Item.objects.create(
            title="Item One",
            kghID=11,
            price=5.45,
            deleted=True
        )

        itemList = [
            self.createCsvRowData(material="11", maPrice="11.50", materialDescription="somethingDifferent"),
            self.createCsvRowData(material="22", maPrice="3.75")
        ]
        response = self.makeCallWithCSV(itemList)

        self.assertMessageLevel(response, self.MESSAGE_SUCCESS)

        itemOne.refresh_from_db()

        self.assertEqual(itemOne.kghID, "11")
        self.assertEqual(itemOne.price, Decimal("5.45"))
        self.assertEqual(itemOne.title, "Item One")
        self.assertEqual(itemOne.deleted, True)

    def test_kghItemsInDatabase_updatesItemsToCorrectValues(self):
        itemOne = Item.objects.create(
            title="Item One",
            kghID=11
        )
        itemTwo = Item.objects.create(
            title="Item Two",
            price="77",
            kghID=22
        )
        itemThree = Item.objects.create(
            title="Item Three",
            price="12",
            kghID=33
        )

        itemList = [
            self.createCsvRowData(material="11", maPrice="11.50", materialDescription="somethingDifferent"),
            self.createCsvRowData(material="22", maPrice="3.75")
        ]
        response = self.makeCallWithCSV(itemList)

        self.assertMessageLevel(response, self.MESSAGE_SUCCESS)

        itemOne.refresh_from_db()
        itemTwo.refresh_from_db()
        itemThree.refresh_from_db()

        self.assertEqual(itemOne.kghID, "11")
        self.assertEqual(itemOne.price, Decimal("11.50"))
        self.assertEqual(itemOne.title, "Item One")

        self.assertEqual(itemTwo.kghID, "22")
        self.assertEqual(itemTwo.price, Decimal("3.75"))

        self.assertEqual(itemThree.kghID, "33")
        self.assertEqual(itemThree.price, Decimal("12"))
    def test_columnOrderDifferent_noErrors(self):
        itemOne = Item.objects.create(
            title="Item One",
            kghID=11
        )

        itemList = [
            ["MA price","Material","Old material no."],
            ["11.50","11",""],
        ]
        response = self.makeCallWithCSV(itemList, addHeader=False)

        self.assertMessageLevel(response, self.MESSAGE_SUCCESS)

        itemOne.refresh_from_db()

        self.assertEqual(itemOne.kghID, "11")
        self.assertEqual(itemOne.price, Decimal("11.50"))
        self.assertEqual(itemOne.title, "Item One")

    def test_kghItemsInDatabase_returnsUpdatedElementsInContext(self):
        itemOne = Item.objects.create(
            title="Item One",
            kghID=11
        )
        itemTwo = Item.objects.create(
            title="Item Two",
            price="77",
            kghID=22
        )
        itemThree = Item.objects.create(
            title="Item Three",
            price="12",
            kghID=33
        )

        itemList = [
            self.createCsvRowData(material="11", maPrice="11.50", materialDescription="somethingDifferent"),
            self.createCsvRowData(material="22", maPrice="3.75")
        ]
        response = self.makeCallWithCSV(itemList)

        self.assertMessageLevel(response, self.MESSAGE_SUCCESS)

        # [kghId, oldKghId, title, oldPrice, newPrice]
        changes = response.context['changes']
        self.assertEqual(len(changes), 2)

        changesOne = next(x for x in changes if x["kghId"] == "11")  # Find the first element with kghId = "11"
        self.assertIsNotNone(changesOne)
        self.assertEqual(changesOne["title"], "Item One")
        self.assertEqual(changesOne["oldPrice"], Decimal(0))
        self.assertEqual(changesOne["newPrice"], Decimal("11.5"))

        changesTwo = next(x for x in changes if x["kghId"] == "22")  # Find the first element with kghId = "22"
        self.assertIsNotNone(changesTwo)
        self.assertEqual(changesTwo["title"], "Item Two")
        self.assertEqual(changesTwo["oldPrice"], Decimal("77"))
        self.assertEqual(changesTwo["newPrice"], Decimal("3.75"))

    def test_noFieldsChange_contextShowsNoChanges(self):
        itemOne = Item.objects.create(
            title="Item One",
            kghID=11,
            price=55
        )

        itemList = [
            self.createCsvRowData(material="11", maPrice="55")
        ]
        response = self.makeCallWithCSV(itemList)

        self.assertMessageLevel(response, self.MESSAGE_SUCCESS)

        # [kghId, oldKghId, title, oldPrice, newPrice]
        changes = response.context['changes']
        self.assertEqual(len(changes), 0)
        self.assertEqual(response.context['catalogUploaded'], True)

    # Old material no. can be presented as one or more numbers separated by a space
    def test_kghOldMaterialNumberSingleElementMatchesItem_updatesItemIdAndProperties(self):
        itemOne = Item.objects.create(
            title="Item One",
            price="3",
            kghID=11
        )

        itemList = [
            self.createCsvRowData(material="25", oldMaterialNumbers="11", maPrice="78"),
        ]
        response = self.makeCallWithCSV(itemList)

        self.assertMessageLevel(response, self.MESSAGE_SUCCESS)

        itemOne.refresh_from_db()

        self.assertEqual(itemOne.kghID, "25")
        self.assertEqual(itemOne.price, Decimal("78"))
        self.assertEqual(itemOne.title, "Item One")

    def test_kghOldMaterialNumberFirstElementMatchesItem_updatesItemIdAndProperties(self):
        itemOne = Item.objects.create(
            title="Item One",
            price="3",
            kghID=11
        )

        itemList = [
            self.createCsvRowData(material="25", oldMaterialNumbers="11 57", maPrice="78"),
        ]
        response = self.makeCallWithCSV(itemList)

        self.assertMessageLevel(response, self.MESSAGE_SUCCESS)

        itemOne.refresh_from_db()

        self.assertEqual(itemOne.kghID, "25")
        self.assertEqual(itemOne.price, Decimal("78"))
        self.assertEqual(itemOne.title, "Item One")

    def test_kghOldMaterialNumberSecondElementMatchesItem_updatesItemIdAndProperties(self):
        itemOne = Item.objects.create(
            title="Item One",
            price="3",
            kghID=11
        )

        itemList = [
            self.createCsvRowData(material="25", oldMaterialNumbers="5447 11", maPrice="78"),
        ]
        response = self.makeCallWithCSV(itemList)

        self.assertMessageLevel(response, self.MESSAGE_SUCCESS)

        itemOne.refresh_from_db()

        self.assertEqual(itemOne.kghID, "25")
        self.assertEqual(itemOne.price, Decimal("78"))
        self.assertEqual(itemOne.title, "Item One")

    def test_kghMaterialIdUpdated_ShowsChangeInContext(self):
        itemOne = Item.objects.create(
            title="Item One",
            price="3",
            kghID=11
        )

        itemList = [
            self.createCsvRowData(material="25", oldMaterialNumbers="57 11", maPrice="78"),
        ]
        response = self.makeCallWithCSV(itemList)

        self.assertMessageLevel(response, self.MESSAGE_SUCCESS)

        changes = response.context['changes']
        self.assertEqual(len(changes), 1)

        changesOne = changes[0]
        self.assertEqual(changesOne["kghId"], "25")
        self.assertEqual(changesOne["oldKghId"], "11")
        self.assertEqual(changesOne["title"], "Item One")
        self.assertEqual(changesOne["oldPrice"], 3)
        self.assertEqual(changesOne["newPrice"], 78)

    def test_onParsingError_noChangesWereMadeAndErrorShown(self):
        itemOne = Item.objects.create(
            title="Item One",
            price=27,
            kghID=11
        )
        itemTwo = Item.objects.create(
            title="Item Two",
            price="77",
            kghID=22
        )
        itemThree = Item.objects.create(
            title="Item Three",
            price="12",
            kghID=33
        )

        itemList = [
            self.createCsvRowData(material="11", maPrice="11.50"),
            self.createCsvRowData(material="22", maPrice="dd"),
            self.createCsvRowData(material="33", maPrice="3.75")
        ]
        response = self.makeCallWithCSV(itemList)

        self.assertMessageLevel(response, self.MESSAGE_ERROR)

        itemOne.refresh_from_db()
        itemTwo.refresh_from_db()
        itemThree.refresh_from_db()

        self.assertEqual(itemOne.kghID, "11")
        self.assertEqual(itemOne.price, Decimal("27"))
        self.assertEqual(itemOne.title, "Item One")

        self.assertEqual(itemTwo.kghID, "22")
        self.assertEqual(itemTwo.price, Decimal("77.0"))

        self.assertEqual(itemThree.kghID, "33")
        self.assertEqual(itemThree.price, Decimal("12"))

    def test_kghItemPriceMissing_throwsExceptionAndMakesNoChanges(self):
        itemOne = Item.objects.create(
            title="Item One",
            price=27,
            kghID=11
        )
        itemTwo = Item.objects.create(
            title="Item Two",
            price="77",
            kghID=22
        )
        itemThree = Item.objects.create(
            title="Item Three",
            price="12",
            kghID=33
        )

        itemList = [
            self.createCsvRowData(material="11", maPrice="11.50"),
            self.createCsvRowData(material="22", maPrice=""), # No price given
            self.createCsvRowData(material="33", maPrice="3.75")
        ]
        response = self.makeCallWithCSV(itemList)

        self.assertMessageLevel(response, self.MESSAGE_ERROR)

        itemOne.refresh_from_db()
        itemTwo.refresh_from_db()
        itemThree.refresh_from_db()

        self.assertEqual(itemOne.kghID, "11")
        self.assertEqual(itemOne.price, Decimal("27"))
        self.assertEqual(itemOne.title, "Item One")

        self.assertEqual(itemTwo.kghID, "22")
        self.assertEqual(itemTwo.price, Decimal("77.0"))

        self.assertEqual(itemThree.kghID, "33")
        self.assertEqual(itemThree.price, Decimal("12"))

    def test_kghItemModelHasNoMatch_contextShowsUnmatchedField(self):
        itemOne = Item.objects.create(
            title="Item One",
            price=3,
            kghID=11
        )

        itemList = [
            self.createCsvRowData(material="999999", maPrice="11.50", materialDescription="somethingDifferent"),
        ]
        response = self.makeCallWithCSV(itemList)

        self.assertMessageLevel(response, self.MESSAGE_SUCCESS)
        self.assertMessageLevel(response, self.MESSAGE_WARNING)

        unmatchedFields =  response.context['unmatchedFields']
        self.assertEqual(len(unmatchedFields), 1)

        unmatchedElement = unmatchedFields[0]

        self.assertEqual(unmatchedElement['kghID'], "11")
        self.assertEqual(unmatchedElement['name'], "Item One")

