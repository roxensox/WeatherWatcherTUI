# WeatherCLI
A TUI for keeping an eye on the weather. Can be configured to update at any interval, and pings weatherapi.com for new info. Requires a user's API key to access WeatherAPI, and does a basic request for current weather conditions at the specified location. Fields of interest can be toggled in the `Config` class's `keys` attribute in `processing.py`.

## Dependencies
- UV
- Python 3.1X
- Python `dotenv` package
- Python `requests` package
- Terminal with UTF-8 font
- Have not tested for Windows, but works on MacOS and probably Linux

## Requirements
- `.env` file with the following line:
```
API_KEY=YOUR-API-KEY
```

## Usage
Run the program using the following command:
```
uv run path/to/main.py
```
When prompted to enter a location, enter the zip code or city name and press `enter`.

Once the Weather window is displayed, you can press the `q` key to exit the program.

## Planned Features
- [ ] Toggleable Fahrenheit/Celsius option
- [ ] Ability to change locations
- [ ] Ability to store previous locations and select them from a dropdown menu
- [ ] Ability to add new APIs to request from and display data dynamically
- [ ] Graphics to represent the weather conditions
