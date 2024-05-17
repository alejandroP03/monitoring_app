import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import Place


# Create your views here.
@csrf_exempt
def creation(request):
    if request.method == "POST":
        body = json.loads(request.body)
        name = body["name"]
        place = Place(name=name)

        place.save()
        return JsonResponse({"id": place.id, "name": place.name})


def list_places(request):
    places = Place.objects.all()
    return JsonResponse(list(places.values()), safe=False)


def get_place(request, place_name):
    place = Place.objects.get(name=place_name)
    if place is None:
        return JsonResponse({})
    return JsonResponse({"id": place.id, "name": place.name})
