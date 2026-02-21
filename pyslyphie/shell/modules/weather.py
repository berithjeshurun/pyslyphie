import openmeteo_requests
import requests_cache
from retry_requests import retry
import pandas as pd


class Weather:
    def __init__(self):
        self.__cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
        self.__retry_session = retry(self.__cache_session, retries=5, backoff_factor=0.2)
        self.__openmeteo = openmeteo_requests.Client(session=self.__retry_session)

    def openMetro(self, lon: float, lat: float):
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": lat,
            "longitude": lon,
            "hourly": "temperature_2m,relativehumidity_2m,precipitation",
            "minutely": "precipitation",
            "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum",
            "current_weather": True,
            "timezone": "auto"
        }

        responses = self.__openmeteo.weather_api(url, params=params)
        if len(responses) < 1:
            return {'status': False, 'error': 'No response from Open-Meteo API'}

        response = responses[0]

        def extract_variables(obj):
            """
            Extract all variables from a VariablesWithTime object into a dict.
            Returns plain lists and adds 'time' as a list of datetime objects.
            """
            data = {}
            j = 0
            while True:
                try:
                    var = obj.Variables(j)
                    name = getattr(var, 'variable', f'var_{j}')
                    data[name] = var.ValuesAsNumpy().tolist()
                    j += 1
                except IndexError:
                    break

            data['time'] = pd.date_range(
                start=pd.to_datetime(obj.Time(), unit="s", utc=True),
                end=pd.to_datetime(obj.TimeEnd(), unit="s", utc=True),
                freq=pd.Timedelta(seconds=obj.Interval()),
                inclusive="left"
            ).to_pydatetime().tolist()

            return data

        hourly_data = extract_variables(response.Hourly())
        minutely_data = extract_variables(response.Minutely()) if response.Minutely() else {}
        daily_data = extract_variables(response.Daily()) if response.Daily() else {}

        current = response.CurrentWeather()
        current_data = {}
        if current:
            current_data = {
                'temperature': current.Temperature(),
                'windspeed': current.Windspeed(),
                'winddirection': current.WindDirection(),
                'weathercode': current.WeatherCode(),
                'time': pd.to_datetime(current.Time(), unit='s', utc=True)
            }

        return {
            'status': True,
            'lat': response.Latitude(),
            'lon': response.Longitude(),
            'elevation': f'{response.Elevation()} m asl',
            'timezone': response.Timezone(),
            'hourly': hourly_data,
            'minutely': minutely_data,
            'daily': daily_data,
            'current': current_data
        }