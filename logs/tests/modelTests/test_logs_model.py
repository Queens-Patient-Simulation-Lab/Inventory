from itemManagement.models import Item, Location
from security.models import User
from logs.models import UserLogs, ItemCountLogs, ItemInfoLogs
import logs.models as Logs
from django.test import TestCase


class UserLogsTest(TestCase):

    def test_inputCorrectLoggingArgumentWithSingleUser_logSuccessfully(self):
        u = User.objects.create_user(email='test@test.com', password='test')
        UserLogs.logging(operator_user=u, logCode=Logs.LOGCODE_000000, logMsg=Logs.LOGMSG_000000)

        self.assertEqual(UserLogs.objects.all().count(), 1)

    def test_inputCorrectLoggingArgumentWithTwoUser_logSuccessfully(self):
        u1 = User.objects.create_user(email='test1@test.com', password='test')
        u2 = User.objects.create_user(email='test2@test.com', password='test')
        UserLogs.logging(operator_user=u1, subject_user=u2, logCode=Logs.LOGCODE_000000, logMsg=Logs.LOGMSG_000000)

        self.assertEqual(UserLogs.objects.all().count(), 1)

    def test_logMutipleLogs_correctNumberOfLogsInDB(self):
        u1 = User.objects.create_user(email='test1@test.com', password='test')
        u2 = User.objects.create_user(email='test2@test.com', password='test')
        UserLogs.logging(operator_user=u1, logCode=Logs.LOGCODE_000000, logMsg=Logs.LOGMSG_000000)
        UserLogs.logging(operator_user=u2, logCode=Logs.LOGCODE_000000, logMsg=Logs.LOGMSG_000000)

        self.assertEqual(UserLogs.objects.all().count(), 2)

    # def test_missingOperator_failToLog(self):
    #     UserLogs.logging(operator_user=None, logCode=Logs.LOGCODE_000000, logMsg=Logs.LOGMSG_000000)
    #
    #     self.assertRaises(Exception, msg='insufficient argument')

    def test_logMutipleLogs_everyLogHasTime(self):
        u1 = User.objects.create_user(email='test1@test.com', password='test')
        u2 = User.objects.create_user(email='test2@test.com', password='test')
        UserLogs.logging(operator_user=u1, logCode=Logs.LOGCODE_000000, logMsg=Logs.LOGMSG_000000)
        UserLogs.logging(operator_user=u2, logCode=Logs.LOGCODE_000000, logMsg=Logs.LOGMSG_000000)

        self.assertEqual(UserLogs.objects.exclude(time=None).count(), 2)



class ItemCountLogsTest(TestCase):
    def test_inputCorrectLoggingArgument_logSuccessfully(self):
        u = User.objects.create_user(email='test@test.com', password='test')
        location = Location.objects.create(name='test location', description='test location description')
        item = Item.objects.create(kghID='xxxxxx', title='test item', description='test item description')
        ItemCountLogs.logging(operator_user=u, item=item, quantity=10, location=location,
                              logCode=Logs.LOGCODE_000000, logMsg=Logs.LOGMSG_000000)

        self.assertEqual(ItemCountLogs.objects.all().count(), 1)

    def test_logMultipleLogs_correctNumberOfLogsInDB(self):
        user = User.objects.create_user(email='test1@test.com', password='test')
        location = Location.objects.create(name='test location 1', description='test location 1 description')
        item1 = Item.objects.create(kghID='xxxxxx', title='test item 1', description='test item 1 description')
        item2 = Item.objects.create(kghID='xxxxxx', title='test item 2', description='test item 2 description')
        ItemCountLogs.logging(operator_user=user, item=item1, quantity=10, location=location,
                              logCode=Logs.LOGCODE_000000, logMsg=Logs.LOGMSG_000000)
        ItemCountLogs.logging(operator_user=user, item=item2, quantity=10, location=location,
                              logCode=Logs.LOGCODE_000000, logMsg=Logs.LOGMSG_000000)

        self.assertEqual(ItemCountLogs.objects.all().count(), 2)

    def test_logMutipleLogs_everyLogHasTime(self):
        user = User.objects.create_user(email='test1@test.com', password='test')
        location = Location.objects.create(name='test location 1', description='test location 1 description')
        item1 = Item.objects.create(kghID='xxxxxx', title='test item 1', description='test item 1 description')
        item2 = Item.objects.create(kghID='xxxxxx', title='test item 2', description='test item 2 description')
        ItemCountLogs.logging(operator_user=user, item=item1, quantity=10, location=location,
                              logCode=Logs.LOGCODE_000000, logMsg=Logs.LOGMSG_000000)
        ItemCountLogs.logging(operator_user=user, item=item2, quantity=10, location=location,
                              logCode=Logs.LOGCODE_000000, logMsg=Logs.LOGMSG_000000)

        self.assertEqual(ItemCountLogs.objects.exclude(time=None).count(), 2)

class ItemInfoLogsTest(TestCase):
    def test_inputCorrectRequiredLoggingArgument_logSuccessfully(self):
        user = User.objects.create_user(email='test1@test.com', password='test')
        item = Item.objects.create(kghID='xxxxxx', title='test item', description='test item description')
        ItemInfoLogs.logging(operator_user=user, item=item, logCode=Logs.LOGCODE_000000, logMsg=Logs.LOGMSG_000000)

        self.assertEqual(ItemInfoLogs.objects.all().count(), 1)

    def test_inputCorrectLoggingArgumentWithPrice_logSuccessfully(self):
        user = User.objects.create_user(email='test1@test.com', password='test')
        item = Item.objects.create(kghID='xxxxxx', title='test item', description='test item description')
        ItemInfoLogs.logging(operator_user=user, item=item, price=40.0,
                             logCode=Logs.LOGCODE_000000, logMsg=Logs.LOGMSG_000000)

        self.assertEqual(ItemInfoLogs.objects.exclude(price=None).count(), 1)

    def test_inputCorrectLoggingArgumentWithKghID_logSuccessfully(self):
        user = User.objects.create_user(email='test1@test.com', password='test')
        item = Item.objects.create(kghID='xxxxxx', title='test item', description='test item description')
        ItemInfoLogs.logging(operator_user=user, item=item, kghID='testid',
                             logCode=Logs.LOGCODE_000000, logMsg=Logs.LOGMSG_000000)

        self.assertEqual(ItemInfoLogs.objects.exclude(kghID=None).count(), 1)

    def test_logMutipleLogs_everyLogHasTime(self):
        user = User.objects.create_user(email='test1@test.com', password='test')
        item = Item.objects.create(kghID='xxxxxx', title='test item', description='test item description')
        ItemInfoLogs.logging(operator_user=user, item=item, logCode=Logs.LOGCODE_000000, logMsg=Logs.LOGMSG_000000)
        ItemInfoLogs.logging(operator_user=user, item=item, price=40.0,
                             logCode=Logs.LOGCODE_000000, logMsg=Logs.LOGMSG_000000)
        ItemInfoLogs.logging(operator_user=user, item=item, kghID='testid',
                             logCode=Logs.LOGCODE_000000, logMsg=Logs.LOGMSG_000000)

        self.assertEqual(ItemInfoLogs.objects.exclude(time=None).count(), 3)