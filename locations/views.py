from django.shortcuts import render
from .models import Location


def locationList(request):
    locations = Location.objects.all().order_by('name')
    return render(request, 'locations.html', {'locations': locations})

