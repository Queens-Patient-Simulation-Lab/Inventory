from django.db import models


class Location(models.Model):

    name = models.CharField(max_length=64)
    description = models.TextField()
    # address = models.CharField
    # roomNumber = models.CharField


def __str__(self):
    return self.name
