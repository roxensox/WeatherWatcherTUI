import requests, json
import importlib.resources as resources
from urllib.parse import urlencode


class Config:
    def __init__(self, API_Key: str, log=None, http_client=None)->None:
        self.API_Key = API_Key
        self.location = ""
        self.saved_locations = 0
        self.log = log
        self.http_client = http_client or requests


    def set_location(self, location: str)->None:
        '''
        Sets the location to be used in future API calls
        '''
        self.location = location


    def build_url(self)->str:
        params = {
            "key":self.API_Key,
            "q":self.location,
            "aqi":"no",
        }
        url = f"http://api.weatherapi.com/v1/current.json{urlencode(params)}"
        return url


    def get_weather(self)->dict:
        '''
        Makes a request to the weather API for the current weather in the specified area, returns it as a dictionary
        '''
        url = self.build_url()
        resp = self.request_weather(url)
        out = {}
        if resp.status_code <= 299:
            out = resp.json()
        resp.close()
        return out


    def request_weather(self, url):
        resp = self.http_client.get(url)
        return resp


    def process_location_reset(self, mainscreen, location):
        data = self.processor.load_data(self.get_weather())
        mainscreen.display_location_info(data=self.processor.filtered_data, heading="Weather")


    def get_saved_locations(self, dbConn):
        self.saved_locations = dbConn.execute("SELECT COUNT(*) FROM locations").fetchone()[0]
        if self.log != None:
            self.log.write(f"Saved: {self.saved_locations}")
        dbConn.close()


class Processor:
    '''
    Class for filtering JSON data
    '''
    def __init__(self):
        self.prefs = {}


    def load_data(self, data: dict)->None:
        '''
        Loads a JSON dictionary into a list of key/pair tuples
        '''

        self.filtered_data = []
        self.filtered_data = self.filter_data_recursive(self.prefs, data, self.filtered_data)


    def filter_data_recursive(self, prefs: dict, data: dict, history: list)->list:
        '''
        Filters data recursively and will work on any JSON with compatible prefs
        '''

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
    '''
    Processor subclass for displaying WeatherAPI information
    '''
    def __init__(self):
        super().__init__()
        self.title = "Weather"

        # Imports preferences from a json file for modular preferences
        root = __package__.split('.')[0]
        cfg_path = resources.files(root).joinpath("../configs/api.json")
        with open(cfg_path, "r") as api_configs:
            data = json.load(api_configs)
        self.prefs = {}
        for k in data.keys():
            if self.title.lower() in k:
                self.prefs = data[k]
