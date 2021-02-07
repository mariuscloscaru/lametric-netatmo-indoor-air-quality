import json, time
import urllib.parse, urllib.request

######################## USER SPECIFIC INFORMATION ######################

# To be able to have a program accessing your netatmo data, you have to register your program as
# a Netatmo app in your Netatmo account. All you have to do is to give it a name (whatever) and you will be
# returned a client_id and secret that your app has to supply to access netatmo servers.

_CLIENT_ID     = ""   # Your client ID from Netatmo app registration at http://dev.netatmo.com/dev/listapps
_CLIENT_SECRET = ""   # Your client app secret   '     '
_USERNAME      = ""   # Your netatmo account username
_PASSWORD      = ""   # Your netatmo account password

#########################################################################


# Common definitions

_BASE_URL            = "https://api.netatmo.com/"
_AUTH_REQ            = _BASE_URL + "oauth2/token"
_GETHOMECOACH_REQ    = _BASE_URL + "api/gethomecoachsdata"


class ClientAuth:
    "Request authentication and keep access token available through token method. Renew it automatically if necessary"

    def __init__(self, clientId=_CLIENT_ID,
                       clientSecret=_CLIENT_SECRET,
                       username=_USERNAME,
                       password=_PASSWORD):

        postParams = {
                "grant_type" : "password",
                "client_id" : clientId,
                "client_secret" : clientSecret,
                "username" : username,
                "password" : password,
                "scope" : "read_homecoach"
                }
        resp = postRequest(_AUTH_REQ, postParams)

        self._clientId = clientId
        self._clientSecret = clientSecret
        self._accessToken = resp['access_token']
        self.refreshToken = resp['refresh_token']
        self._scope = resp['scope']
        self.expiration = int(resp['expire_in'] + time.time())

    @property
    def accessToken(self):

        if self.expiration < time.time(): # Token should be renewed
            postParams = {
                    "grant_type" : "refresh_token",
                    "refresh_token" : self.refreshToken,
                    "client_id" : self._clientId,
                    "client_secret" : self._clientSecret
                    }
            resp = postRequest(_AUTH_REQ, postParams)

            self._accessToken = resp['access_token']
            self.refreshToken = resp['refresh_token']
            self.expiration = int(resp['expire_in'] + time.time())

        return self._accessToken

class HomeCoach:
    "Request data from indoor air monitor"

    def __init__(self, authData):

        self.getAuthToken = authData.accessToken
        headers = { 
            "Content-Type" : "application/json",
            "Authorization" : "Bearer " + self.getAuthToken 
            }
        resp = getRequest(_GETHOMECOACH_REQ, headers)
        self.rawData = resp['body']
        self.stations = { d['_id'] : d for d in self.rawData['devices'] }
        self.default_station = list(self.stations.values())[0]['station_name']
        self.user = self.rawData['user']

    def getTemperature(self, station=None):
        if not station : station = self.default_station
        for i,s in self.stations.items():
            if s['station_name'] == station : return s['dashboard_data']['Temperature']
        return None

    def getHumidity(self, station=None):
        if not station : station = self.default_station
        for i,s in self.stations.items():
            if s['station_name'] == station : return s['dashboard_data']['Humidity']
        return None

    def getCO2(self, station=None):
        if not station : station = self.default_station
        for i,s in self.stations.items():
            if s['station_name'] == station : return s['dashboard_data']['CO2']
        return None

# Utilities routines

def postRequest(url, params):
    req = urllib.request.Request(url)
    req.add_header("Content-Type","application/x-www-form-urlencoded;charset=utf-8")
    params = urllib.parse.urlencode(params).encode('utf-8')
    resp = urllib.request.urlopen(req, params).read().decode("utf-8")
    return json.loads(resp)

def getRequest(url, headers):
    req = urllib.request.Request(url=url, headers=headers)
    try:
        resp = urllib.request.urlopen(req).read().decode("utf-8")
    except urllib.error.HTTPError as e:
        print(e.code)
        print(e.read()) 
    return json.loads(resp)
