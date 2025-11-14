from processing.processing_classes import Config


def test_ConfigAppliesInputs():
    cfg = Config("DUMMY_KEY")
    cfg.set_location("12345")
    url = cfg.build_url()
    assert "key=DUMMY_KEY" in url
    assert "q=12345" in url
    assert url.startswith("http://api.weatherapi.com/v1/current.json")


class FakeDBConn:
    def __init__(self):
        self.queries = []
        self.closed = False


    def execute(self, query):
        self.queries.append(query)
        return FakeCursor(results=[(10,)])


    def close(self):
        self.closed = True


class FakeCursor:
    def __init__(self, results = None):
        self.results = results or []


    def fetchone(self):
        return self.results.pop() if len(self.results) > 0 else ()


    def fetchall(self):
        return self.results


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


def test_Config_set_location():
    '''
    Tests functionality of the set_location method when it's successful
    '''
    cfg = Config("DUMMY_KEY")
    cfg.set_location("58401")
    assert cfg.location == "58401"
    cfg.set_location("")
    assert cfg.location == ""


def test_Config_get_weather_success():
    '''
    Tests functionality of the get_weather method
    '''
    client = FakeClient(payload={"temp_f":71.5})
    cfg = Config("DUMMY_KEY", http_client = client)
    weather = cfg.get_weather()
    assert weather["temp_f"] == 71.5
    response = cfg.request_weather(client.calls[0])
    assert response.status_code == 200
    assert response.payload == {"temp_f":71.5}


def test_Config_get_weather_failure():
    '''
    Tests functionality of the get_weather method
    '''
    client = FakeClient(401, {"ERROR":"UNAUTHORIZED"})
    cfg = Config("DUMMY_KEY", http_client = client)
    weather = cfg.get_weather()
    assert weather == {}


def test_Config_get_saved_locations():
    cfg = Config("DUMMY_KEY")
    dbConn = FakeDBConn()
    result_count = cfg.get_saved_locations(dbConn)
    assert dbConn.closed
    assert dbConn.queries[0] == "SELECT COUNT(*) FROM locations"
    assert cfg.saved_locations == 10
