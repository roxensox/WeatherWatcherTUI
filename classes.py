import requests, curses


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
        out = None
        if resp.status_code <= 299:
            out = resp.json()
        resp.close()
        return out


class Printer:
    def __init__(self):
            self.keys = {
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


    def load_data(self, data: dict)->None:
        self.data = data
        self.filter_data()


    def filter_data(self)->None:
        self.filtered_data = []
        for k in self.keys:
            k_tier = self.keys[k]
            d_tier = self.data[k]
            for k1 in k_tier:
                if type(k_tier[k1]) != tuple:
                    k1_tier = k_tier[k1]
                    d1_tier = d_tier[k1]
                    for k2 in k1_tier:
                        if k1_tier[k2][0]:
                            self.filtered_data.append((k1_tier[k2][1], d1_tier[k2]))
                elif k_tier[k1][0]:
                    self.filtered_data.append((k_tier[k1][1], d_tier[k1]))


    def output_data(self)->None:
        tick = True
        strings = [f"{i[0]}: {i[1]}" for i in self.filtered_data]
        lengths = [len(i) for i in strings]
        for s in strings:
            spacer = " " * ((max(lengths) - len(s)) + 1)
            if tick == True:
                pass
                #print(s, end=spacer)
            else:
                pass
                #print(s)
            tick = not tick
