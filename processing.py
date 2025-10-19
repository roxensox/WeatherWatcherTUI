import requests, curses, _curses
from interface import MainInterface


class Config:
    def __init__(self, API_Key: str)->None:
        self.API_Key = API_Key
        self.location = ""


    def set_location(self, location: str)->None:
        '''
        Sets the location to be used in future API calls
        '''
        self.location = location


    def get_weather(self)->dict:
        '''
        Makes a request to the weather API for the current weather in the specified area, returns it as a dictionary
        '''
        resp = requests.get(f"http://api.weatherapi.com/v1/current.json?key={self.API_Key}&q={self.location}&aqi=no")
        out = {}
        if resp.status_code <= 299:
            out = resp.json()
        resp.close()
        if out == {}:
            raise ValueError(f"No data retrieved")
        return out


class Processor:
    # Class for filtering JSON data
    def __init__(self):
        self.prefs = {}


    def load_data(self, data: dict)->None:
        self.filtered_data = []
        self.filtered_data = self.filter_data_recursive(self.prefs, data, self.filtered_data)


    def filter_data_recursive(self, prefs: dict, data: dict, history: list)->list:
        # Filters data recursively and will work on any JSON with compatible prefs

        for k in prefs.keys():
            # Checks for corresponding value in data dict, skips key if it's not there
            if data.get(k) == None:
                continue
            # Filters recursively if the value is a dictionary
            if type(prefs[k]) == dict:
                history = self.filter_data_recursive(prefs[k], data[k], history)
            # Adds value to output if it's toggled on
            elif prefs[k][0] == True:
                history.append((prefs[k][1], str(data[k])))
        return history


class WeatherProcessor (Processor):
    # Processor subclass for displaying WeatherAPI information
    def __init__(self):
        super().__init__()
        self.prefs = {
            "location": {
                "name":(True,"City"),
                "region":(True,"State/Province"),
                "country":(True,"Country"),
                "lat":(False,"Latitude"),
                "lon":(False,"Longitude"),
                "tz_id":(True,"Timezone"),
                "localtime_epoch":(False,"Local Time UTC"),
                "localtime":(True,"Local Time"),
            },
            "current":{
                "condition": {
                    "text":(True,"Condition"),
                    "icon":(False,"Icon URL"),
                    "code":(False,"Condition Code"),
                },
                "last_updated_epoch":(False,"Last Updated UTC"),
                "last_updated":(True,"Last Updated"),
                "temp_c":(True,"Temperature C"),
                "temp_f":(True,"Temperature F"),
                "is_day":(True,"Daytime"),
                "wind_mph":(True,"Wind Speed (MPH)"),
                "wind_kph":(False,"Wind Speed (KPH)"),
                "wind_degree":(False,"Wind Degree"),
                "wind_dir":(True,"Wind Direction"),
                "pressure_mb":(False,"Pressure (mb)"),
                "pressure_in":(False,"Pressure (in)"),
                "precip_mm":(False,"Precipitation (mm)"),
                "precip_in":(True,"Precipitation (in)"),
                "humidity":(True,"Humidity"),
                "cloud":(False,"Cloud Cover"),
                "feelslike_c":(False,"Feels Like C"),
                "feelslike_f":(True,"Feels Like F"),
                "windchill_c":(False,"Windchill C"),
                "windchill_f":(True,"Windchill F"),
                "heatindex_c":(False,"Heat Index C"),
                "heatindex_f":(True,"Heat Index F"),
                "dewpoint_c":(False,"Dew Point C"),
                "dewpoint_f":(True,"Dew Point F"),
                "vis_km":(False,"Visibility (km)"),
                "vis_miles":(True,"Visibility (mi)"),
                "uv":(True,"UV Index"),
                "gust_mph":(True,"Gust (MPH)"),
                "gust_kph":(False,"Gust (KPH)"),
                "short_rad":(False,"Short Rad"),
                "diff_rad":(False,"Diff Rad"),
                "dni":(False,"DNI"),
                "gti":(False,"GTI"),
            },
    }

