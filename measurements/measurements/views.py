import json

import requests
from django.conf import settings
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse

from .models import Measurement


def check_variable(data):
    r = requests.get(settings.PATH_VAR, headers={"Accept": "application/json"})
    variables = r.json()

    for variable in variables:
        if data["variable"] == variable["id"]:
            return True

    return False


def check_place(data):
    r_places = requests.get(
        settings.PATH_PLACES + "/" + str(data["place"]),
        headers={"Accept": "application/json"},
    )
    place = r_places.json()
    if "id" in place:
        return True
    return False


def MeasurementList(request):
    queryset = Measurement.objects.all()
    context = list(
        queryset.values("id", "variable", "value", "unit", "place", "dateTime")
    )
    return JsonResponse(context, safe=False)


def MeasurementCreate(request):
    if request.method == "POST":
        data = request.body.decode("utf-8")
        data_json = json.loads(data)
        if check_variable(data_json) == True:
            measurement = Measurement()
            measurement.variable = data_json["variable"]
            measurement.value = data_json["value"]
            measurement.unit = data_json["unit"]
            measurement.place = data_json["place"]
            measurement.save()
            return HttpResponse("successfully created measurement")
        else:
            return HttpResponse(
                "unsuccessfully created measurement. Variable does not exist"
            )


def MeasurementsCreate(request):
    if request.method == "POST":
        data = request.body.decode("utf-8")
        data_json = json.loads(data)
        measurement_list = []
        for measurement in data_json:
            if check_variable(measurement) and check_place(measurement):
                db_measurement = Measurement()
                db_measurement.variable = measurement["variable"]
                db_measurement.value = measurement["value"]
                db_measurement.unit = measurement["unit"]
                db_measurement.place = measurement["place"]
                measurement_list.append(db_measurement)
            else:
                return HttpResponse(
                    "unsuccessfully created measurement. Variable does not exist"
                )

        Measurement.objects.bulk_create(measurement_list)
        return HttpResponse("successfully created measurements")
