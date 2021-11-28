import json
import os

import requests
from requests.adapters import HTTPAdapter, Retry

from social_app.exceptions import APIKeyNotFound

email_validation_api_key = os.getenv("abstract_api_email_validation_api_key")
ip_geolocation_api_key = os.getenv("abstract_api_ip_geolocation_api_key")
holidays_api_key = os.getenv("abstract_api_holidays_api_key")

request_session = requests.Session()
retries = Retry(total=3, backoff_factor=1, status_forcelist=[502, 503, 504])
request_session.mount("https://", HTTPAdapter(max_retries=retries))


def is_email_valid_format(email: str) -> bool:
    return _validate_email_with_abstract_api(email)


def get_geolocation_data_from_ip_address(ip_address: str):
    return _get_geolocation_data_with_abstract_api(ip_address=ip_address)


def get_holiday_data_from_geolocation(country_code, year, month, day):
    return _get_holiday_data_with_abstract_api(
        country_code=country_code, year=year, month=month, day=day
    )


def _validate_email_with_abstract_api(email):
    url = "https://emailvalidation.abstractapi.com/v1"
    if email_validation_api_key is None:
        raise APIKeyNotFound(message="email validation api key not found")
    response = request_session.get(
        f"{url}/?api_key={email_validation_api_key}&email={email}"
    )
    data = json.loads(response.content)
    return data["is_valid_format"]["value"]


def _get_geolocation_data_with_abstract_api(ip_address):
    url = "https://ipgeolocation.abstractapi.com/v1"
    if ip_geolocation_api_key is None:
        raise APIKeyNotFound(message="geolocation api key not found")
    response = requests.get(
        f"{url}/?api_key={ip_geolocation_api_key}&ip_address={ip_address}"
    )
    data = json.loads(response.content)
    location_data: dict = {}
    location_data["city"] = data["city"]
    location_data["region"] = data["region"]
    location_data["country"] = data["country"]
    location_data["country_code"] = data["country_code"]
    location_data["continent"] = data["continent"]
    location_data["continent_code"] = data["continent_code"]
    location_data["longitude"] = data["longitude"]
    location_data["latitude"] = data["latitude"]
    return location_data


def _get_holiday_data_with_abstract_api(
    country_code: str, year: int, month: int, day: int
):
    url = "https://holidays.abstractapi.com/v1"
    if holidays_api_key is None:
        raise APIKeyNotFound(message="holidays api key not found")
    response = requests.get(
        f"{url}/?api_key={holidays_api_key}&country={country_code}&year={year}&month={month}&day={day}"
    )
    data = json.loads(response.content)
    if data < 1:
        return None
    data = data[0]
    holiday_data: dict = {}
    holiday_data["name"] = data["name"]
    holiday_data["description"] = data["description"]
    holiday_data["location"] = data["location"]
    holiday_data["type"] = data["type"]
    holiday_data["date"] = data["date"]
    holiday_data["week_day"] = data["week_day"]
    return holiday_data
