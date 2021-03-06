from django.db import models

# Create your models here.
#TODO: Set field restrictions to more well considered values

# ID is created as primary key by default
from django.db.models import Count, Sum
from django.utils import timezone


class Location(models.Model):
    name = models.CharField(max_length=40, blank=False)
    description = models.TextField(blank=True)
    deleted = models.BooleanField(default=False)

    def getLocationDetailsForItem(self, item):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'quantity' : self.itemstorage_set.get(item=item).quantity
        }

class Item(models.Model):
    kghID = models.CharField(max_length=20, null=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    unit = models.CharField(max_length=20, null=True)
    # Note I don't call now() - It will be called when the object is created
    lastUsed = models.DateTimeField(default=timezone.now)
    price = models.DecimalField(max_digits=7, decimal_places=2, null=True, default=0)
    deleted = models.BooleanField(default=False)
    alertThreshold = models.PositiveSmallIntegerField(default=0)
    alertWhenLow = models.BooleanField(default=False)
    locations = models.ManyToManyField(Location, through='ItemStorage')


    @property
    def totalQuantity(self):
        # return sum(location.count for location in self.locations.all())
        return self.locations.aggregate(Sum('itemstorage__quantity'))['itemstorage__quantity__sum'] or 0

    @property
    def needToNotifyAdmin(self):
        return self.alertWhenLow and self.totalQuantity <= self.alertThreshold

    def getItemSummary(self):
        return {
                'itemId': self.id,
                'name': self.title,
                'locations': [x.name for x in self.locations.all()],
                'totalQuantity': self.totalQuantity,
                'images': self.photo_set
            }
    def getItemDetails(self):
        return {
            'itemId': self.id,
            'name': self.title,
            'kghId': self.kghID,
            'description' : self.description,
            'tags': [x.name for x in self.tag_set.all()],
            'images': self.photo_set,
            'price': self.price,
            'unit': self.unit,
            'parLevel': self.alertThreshold,
            'alertWhenLow': self.alertWhenLow,
            'locations': [x.getLocationDetailsForItem(self) for x in self.locations.all()],
            'totalQuantity': self.totalQuantity
        }


# TODO: Set primary keys
class ItemStorage(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField()
    # TODO:    No idea what displayed field is


class Photo(models.Model):
    mimeType = models.CharField(max_length=20)
    data = models.BinaryField()
    order = models.PositiveSmallIntegerField()
    depicts = models.ForeignKey(Item, on_delete=models.CASCADE)
    class Meta:
        ordering = ["order"]


class Tag(models.Model):
    name = models.CharField(max_length=20)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    class Meta:
        unique_together = ['name', 'item']


