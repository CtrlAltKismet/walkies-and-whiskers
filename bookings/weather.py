"""Weather guidance helpers for outdoor bookings."""

from datetime import date

import requests
from django.conf import settings


WEATHER_API_URL = "https://api.weatherapi.com/v1/forecast.json"
SERVICE_LOCATION = "Coventry"
FORECAST_DAYS = 3

FALLBACK_MESSAGE = (
    "Weather guidance is currently unavailable, but you can still "
    "complete your booking."
)

FUTURE_MESSAGE = (
    "Weather guidance is not yet available for this date. "
    "Please check again closer to your booking."
)


def get_weather_guidance(booking_date):
    """Return Coventry weather guidance for an outdoor booking."""

    days_until_booking = (booking_date - date.today()).days

    if days_until_booking < 0:
        return FALLBACK_MESSAGE

    if days_until_booking >= FORECAST_DAYS:
        return FUTURE_MESSAGE

    if not settings.WEATHER_API_KEY:
        return FALLBACK_MESSAGE

    params = {
        "key": settings.WEATHER_API_KEY,
        "q": SERVICE_LOCATION,
        "days": FORECAST_DAYS,
        "aqi": "no",
        "alerts": "no",
    }

    try:
        response = requests.get(
            WEATHER_API_URL,
            params=params,
            timeout=10,
        )
        response.raise_for_status()

        data = response.json()

        forecast_days = data["forecast"]["forecastday"]

        booking_forecast = next(
            (
                forecast
                for forecast in forecast_days
                if forecast["date"] == booking_date.isoformat()
            ),
            None,
        )

        if booking_forecast is None:
            return FUTURE_MESSAGE

        day = booking_forecast["day"]

        condition = day["condition"]["text"]
        maximum_temperature = day["maxtemp_c"]
        chance_of_rain = day.get("daily_chance_of_rain", 0)

        return build_weather_message(
            condition=condition,
            maximum_temperature=maximum_temperature,
            chance_of_rain=chance_of_rain,
        )

    except (
        requests.RequestException,
        KeyError,
        TypeError,
        ValueError,
    ):
        return FALLBACK_MESSAGE


def build_weather_message(
    condition,
    maximum_temperature,
    chance_of_rain,
):
    """Convert forecast data into friendly pet-care guidance."""

    if chance_of_rain >= 60:
        return (
            f"{condition} is forecast in Coventry, with a "
            f"{chance_of_rain}% chance of rain. Please leave a towel "
            "available after outdoor care."
        )

    if maximum_temperature >= 25:
        return (
            f"{condition} is forecast in Coventry, with temperatures "
            f"reaching approximately {maximum_temperature}°C. "
            "Shaded routes and additional water may be used."
        )

    if maximum_temperature <= 5:
        return (
            f"{condition} is forecast in Coventry, with temperatures "
            f"reaching approximately {maximum_temperature}°C. "
            "Please provide any suitable coat your pet normally wears."
        )

    return (
        f"{condition} is forecast in Coventry, with temperatures "
        f"reaching approximately {maximum_temperature}°C. "
        "No significant weather-related changes are currently expected."
    )