from django.db import models
from itemManagement.models import Item, Location
from security.models import User
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.db.models import Q
import re

class Log(models.Model):
   # the format of the template is "text {type} text ..." with possible types item, user, location and string. up to 5 args are supported
    template = models.CharField(max_length=1024)
    time = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # ideally template arguments would be stored in another model that had the form (itemLog, argNumber, data)
    # However, for cost reasons we are attempting to keep the number of rows down. Logs represent the biggest row contributer and a 5x increase in that number would be expensive
    arg1 = models.CharField(max_length=200, null=True, db_index=True)
    arg2 = models.CharField(max_length=200, null=True, db_index=True)
    arg3 = models.CharField(max_length=200, null=True, db_index=True)
    arg4 = models.CharField(max_length=200, null=True, db_index=True)
    arg5 = models.CharField(max_length=200, null=True, db_index=True)
    class Meta:
        ordering = ["-time"]


    def __render_arg(self, data, type, itemRenderer=None, locationRenderer=None, userRenderer=None):
        data = data[data.index(":")+1:] #remove the namespace
        if type == "string":
            return data
        if type == "user":
            user = User.objects.get(pk=data)
            if userRenderer:
                return userRenderer(user)
            return user.name
        if type == "item":
            item = Item.objects.get(pk=data)
            if itemRenderer:
                return itemRenderer(item)
            return item.title
        if type == "location":
            location = Location.objects.get(pk=data)
            if locationRenderer:
                return locationRenderer(location)
            return location.name
        raise ValidationError(type + " is not a valid log template type")

    def to_string(self, itemRenderer=None, userRenderer=None, locationRenderer=None):
        tokens = re.split("({.*?})", self.template)
        result = ""
        arg = 0
        for token in tokens:
            if not token.startswith("{"):
                result += token
            else:
                arg += 1
                type = token[1:-1]
                data = self.__dict__["arg"+str(arg)]
                result += self.__render_arg(data, type, itemRenderer, locationRenderer, userRenderer)
        return result

    @classmethod
    def __get_storable_value(cls, type, data):
        result = type + ":"
        if type == "string":
            return result + str(data)
        if type == "user" or type == "item" or type == "location":
            return result + str(data.pk)
        raise ValidationError(type + " is not a valid log template type")


    @classmethod
    def log(cls, user, template, *argv):
        types = re.findall(r"{(.*?)}", template)
        entry = Log(user=user, template=template)
        arg = 0
        for type in types:
            entry.__dict__["arg"+str(arg+1)] = cls.__get_storable_value(type, argv[arg])
            arg += 1
        entry.save()

    @classmethod
    def get_logs_for_user(cls, user):
        target = "user:"+str(user.pk)
        query = Q(user=user) | Q(arg1=target) | Q(arg2=target) | Q(arg3=target) | Q(arg4=target) | Q(arg5=target)
        return Log.objects.filter(query)

    @classmethod
    def get_logs_for_item(cls, item):
        target = "item:"+str(item.pk)
        query = Q(arg1=target) | Q(arg2=target) | Q(arg3=target) | Q(arg4=target) | Q(arg5=target)
        return Log.objects.filter(query)



# legacy, needed to not break migrations
def validate_notNone(value):
    if value is None:
        raise ValidationError("value is None")