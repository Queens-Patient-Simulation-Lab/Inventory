from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand

from itemManagement.models import Location, Item, Photo, ItemStorage
from security.models import User


class Command(BaseCommand):
    args = ''
    help = 'Populates development databases with fake data'

    def _overwrite_db(self):
        if not getattr(settings, "DEBUG", False):
            raise Exception("ERROR: Can't run in production")

        call_command('flush')  # Clears the entire db

        # Create a test user

        print("Making new user")
        user = User.objects.create_user("a@a.com", "abcd")
        assert user.password != "abcd"

        mainStorage = Location.objects.create(name="Main Storage Area")
        kennel = Location.objects.create(name="Kennel")

        itemOne = Item.objects.create(
            title="NaCl 0.9% 500ml",
            description="itemOne"
        )
        itemTwo = Item.objects.create(
            title="Puppy",
            description="item Two"

        )
        itemThree = Item.objects.create(
            title="Puppy 2",
            description="item Three"
        )

        ItemStorage.objects.create(item=itemOne, location=mainStorage, quantity=15)
        ItemStorage.objects.create(item=itemTwo, location=kennel, quantity=385)
        ItemStorage.objects.create(item=itemThree, location=kennel, quantity=50)

        Photo.objects.create(
            mimeType="jpg",
            data='itemManagement/nacl.jpg',
            order=1,
            depicts=itemOne
        )
        Photo.objects.create(
            mimeType="jpeg",
            data='itemManagement/puppy.jpeg',
            order=1,
            depicts=itemTwo
        )
        Photo.objects.create(
            mimeType="jpeg",
            data='itemManagement/puppy2.jpeg',
            order=1,
            depicts=itemThree
        )

    def handle(self, *args, **options):
        self._overwrite_db()
