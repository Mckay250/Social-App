from __future__ import absolute_import, unicode_literals

from datetime import date

from celery import shared_task

from . import utils
from .serializers import GeoLocationSerializer, UserHolidayDataSerializer


@shared_task
def populate_user_geo_location_data(user):
    geolocation_data = utils.get_geolocation_data_from_ip_address(user["ip_address"])
    print("geolocation data here >>>>>> ", geolocation_data)
    serializer = GeoLocationSerializer(data=geolocation_data)
    serializer.is_valid(raise_exception=True)
    serializer.save(user=user)
    user_geolocation = serializer.validated_data
    populate_user_Holiday_data(user_geolocation, user)


def populate_user_Holiday_data(geolocation_data, user):
    todays_date = date.today()
    holiday_data = utils.get_holiday_data_from_geolocation(
        geolocation_data["country_code"],
        todays_date.year,
        todays_date.month,
        todays_date.day,
    )
    if holiday_data is None:
        return
    serializer = UserHolidayDataSerializer(data=holiday_data)
    serializer.is_valid(raise_exception=True)
    serializer.save(user)
    return


@shared_task
# @app.task(bind=True)
def add(x, y):
    return 1 + 2
