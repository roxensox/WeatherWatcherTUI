import requests


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
        if resp.status_code <= 299:
            out = resp.json()
        resp.close()
        return out

