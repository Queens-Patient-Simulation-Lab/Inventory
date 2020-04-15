from django.db import models
from itemManagement.models import Item, Location
from security.models import User
from django.utils import timezone
from django.core.exceptions import ValidationError

# log codes are 6 digits number
LOGCODE_000000 = '000000'
LOGMSG_000000 = 'Success'
LOGCODE_999999 = '999999'
LOGMSG_999999 = 'Failure'

LOGCODE_100001 = '100001'
LOGMSG_100001 = 'user create'
LOGCODE_100002 = '100002'
LOGMSG_100002 = 'user delete'
LOGCODE_100003 = '100003'
LOGMSG_100003 = 'change alert status'
LOGCODE_100005 = '100005'
LOGMSG_100005 = 'set subject to admin'
LOGCODE_100006 = '100006'
LOGMSG_100006 = 'set subject to lab assistant'

LOGCODE_STOCKCHANGE = '200001'
LOGMSG_STOCKCHANGE = 'item stock changed'

LOGCODE_CHANGEITEM = '300000'
LOGMSG_CHANGEITEM = 'item details changed'

LOGCODE_CREATEITEM = '300001'
LOGMSG_CREATEITEM = 'created item'
LOGCODE_DELETEITEM = '300002'
LOGMSG_DELETEITEM = 'deleted item'
LOGCODE_300003 = '300003'
LOGMSG_300003 = 'change item KGH ID'
LOGCODE_300004 = '300004'
LOGMSG_300004 = 'change item title'
LOGCODE_300005 = '300005'
LOGMSG_300005 = 'change item description'
LOGCODE_300006 = '300006'
LOGMSG_300006 = 'change item unit of measure'
LOGCODE_300007 = '300007'
LOGMSG_300007 = 'change item price'
LOGCODE_300008 = '300008'
LOGMSG_300008 = 'add a tag'
LOGCODE_300009 = '300009'
LOGMSG_300009 = 'delete a tag'
LOGCODE_300010 = '300010'
LOGMSG_300010 = 'change item par level'
LOGCODE_300011 = '300011'
LOGMSG_300011 = 'add a location'
LOGCODE_300012 = '300012'
LOGMSG_300012 = 'delete a location'
LOGCODE_300013 = '300013'
LOGMSG_300013 = 'add a photo'
LOGCODE_300014 = '300014'
LOGMSG_300014 = 'delete a photo'

def validate_notNone(value):
    if value is None:
        raise ValidationError("value is None")

# Create your models here.
# LogCode pattern: 1XXXXX
class UserLogs(models.Model):
    time = models.DateTimeField(default=timezone.now, validators=[validate_notNone])  # the time when a log is created (required)
    operator_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='operator', validators=[validate_notNone])  # the user who perform the operation (change password, etc.) (required)
    subject_user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='subject')  # the user whose account information is changed by another user (set permission role)
    logCode = models.CharField(max_length=1024, validators=[validate_notNone])  # a special log code for an operation (required)
    logMsg = models.CharField(max_length=1024)  # a special log massage for an operation (required)

    # input the parameters which are applicable
    '''
    Log operations related to user account into database
    input
        operator_user, logCode and logMsg are required
        subject_user is optional. It can be applied when operator change subject user's information
    output
        
    '''
    def logging(operator_user, logCode, logMsg, subject_user=None, *args, **kwargs):
        if operator_user and logCode and logMsg:  # check required parameter
            userLog = UserLogs(operator_user=operator_user, subject_user=subject_user, logCode=logCode, logMsg=logMsg)
            userLog.save()
        else:
            raise Exception('insufficient argument')



# LogCode pattern: 2XXXXX
class ItemCountLogs(models.Model):
    time = models.DateTimeField(default=timezone.now)  # the time when a log is created (required)
    quantity = models.SmallIntegerField()  # the changed quantity of an item  (required)
    operator_user = models.ForeignKey(User,
                             on_delete=models.CASCADE)  # the user who perform the operation (increment/decrement stock) (required)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)  # the item is changed by a user (required)
    location = models.ForeignKey(Location,
                                 on_delete=models.CASCADE)  # the location where the item quantity is changed (required)
    logCode = models.CharField(max_length=1024)  # a special log code for an operation (required)
    logMsg = models.CharField(max_length=1024)  # a special log massage for an operation (required)

    # input the parameters which are applicable
    '''
    Log operations related to item stock into database
    input
        operator_user, item, quantity, location, logCode and logMsg are required
    output

    '''
    def logging(operator_user, item, quantity, location, logCode, logMsg):
        if operator_user and quantity is not None and item and location and logCode and logMsg:  # check required parameter
            itemCountLogs = ItemCountLogs(operator_user=operator_user, item=item, quantity=quantity,
                                          location=location, logCode=logCode, logMsg=logMsg)
            itemCountLogs.save()
        else:
            raise Exception('insufficient argument')


# LogCode pattern: 3XXXXX
class ItemInfoLogs(models.Model):
    time = models.DateTimeField(default=timezone.now)  # the time when a log is created (required)
    kghID = models.CharField(max_length=20, null=True, blank=True)  # the new KGH ID of the item
    price = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True, default=0)  # the new price of the item
    operator_user = models.ForeignKey(User,
                             on_delete=models.CASCADE)  # the user who perform the operation (change item information, item title, etc.) (required)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)  # the item is changed by a user (required)
    logCode = models.CharField(max_length=1024)  # a special log code for an operation (required)
    logMsg = models.CharField(max_length=1024)  # a special log massage for an operation (required)

    # input the parameters which are applicable
    '''
    Log operations related to item information into database
    input
        operator_user, item, logCode and logMsg are required
        kghID is optional. It is applied when operator change a item's kghID
        price is optional. It is applied when operator change a item's price
    output

    '''
    def logging(operator_user, item, logCode, logMsg, kghID=None, price=None):
        if operator_user and item and logCode and logMsg:  # check required parameter
            itemInfoLogs = ItemInfoLogs(operator_user=operator_user, item=item, kghID=kghID, price=price, logCode=logCode, logMsg=logMsg)
            itemInfoLogs.save()
        else:
            raise Exception('insufficient argument')

