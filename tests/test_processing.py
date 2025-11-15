from processing.processing_classes import Config
import pytest


class FakeClient:
    '''
    Class to spoof the requests module for testing
    '''
    def __init__(self, status_code=200, payload=None):
        self.calls = []
        self.status_code = status_code
        self.payload = payload or {}

    def get(self, url):
        self.calls.append(url)
        return FakeResponse(self.status_code, self.payload)


class FakeResponse:
    '''
    Class to spoof the requests.Response class for testing
    '''
    def __init__(self, status_code, payload=None):
        self.status_code = status_code
        self.payload = payload or {}
        self.closed = False

    def json(self):
        return self.payload

    def close(self):
        self.closed = True


@pytest.mark.parametrize(
    "location,status_code,payload,expected_result",
    [
        ("58401",       200, {"temp_f": 71.5}, {"temp_f": 71.5}),   # API_T1
        ("Los Angeles", 200, {"temp_f": 65.0}, {"temp_f": 65.0}),   # API_T2
        ("",            200, {"temp_f": 71.5}, {"temp_f": 71.5}),   # API_T3
        ("",            200, {"temp_f": 71.5,"temp_c":20.5}, 
                             {"temp_f": 71.5,"temp_c":20.5}),       # API_T4
        ("58401",       401, {"error": "unauthorized"}, {}),        # API_T5
        ("58401",       403, {"error": "forbidden"}, {}),           # API_T6
        ("58401",       500, {"error": "server error"}, {}),        # API_T7
    ],
    ids=["API_T1", "API_T2", "API_T3", "API_T4", "API_T5", "API_T6", "API_T7"],
)
def test_get_weather_matrix(location, status_code, payload, expected_result):
    '''
    Tests method's behavior across success/failure conditions
    '''
    client = FakeClient(status_code=status_code, payload=payload)
    cfg = Config("DUMMY_KEY", http_client=client)
    cfg.set_location(location)

    result = cfg.get_weather()

    # Matrix expectations:
    assert isinstance(result, dict)
    assert result == expected_result
    assert len(client.calls) == 1
    assert result != None


@pytest.mark.parametrize(
    "payload",
    [
        {},                          # API_T8: empty dict
        {"temp_c": 22.0},            # API_T9: unexpected key
    ],
    ids=["API_T8_empty_dict", "API_T9_unexpected_key"],
)
def test_get_weather_handles_unexpected_json_shapes(payload):
    client = FakeClient(status_code=200, payload=payload)
    cfg = Config("DUMMY_KEY", http_client=client)
    cfg.set_location("58401")

    result = cfg.get_weather()

    assert isinstance(result, dict)


@pytest.mark.parametrize(
    "location,expected_substrings",
    [
        ("58401",      ["key=DUMMY_KEY", "q=58401"]),       # URL_T1
        ("Los Angeles",["key=DUMMY_KEY", "q=Los+Angeles"]), # URL_T2
        ("",           ["key=DUMMY_KEY", "q="]),            # URL_T3
    ],
    ids=["URL_T1", "URL_T2", "URL_T3"],
)
def test_get_weather_builds_correct_url(location, expected_substrings):
    '''
    Tests method's effectiveness at building URLs
    '''
    client = FakeClient(status_code=200, payload={"temp_f": 71.5})
    cfg = Config("DUMMY_KEY", http_client=client)
    cfg.set_location(location)

    cfg.get_weather()

    assert len(client.calls) == 1
    url = client.calls[0]
    assert url.startswith("http://api.weatherapi.com/v1/current.json")
    for piece in expected_substrings:
        assert piece in url
