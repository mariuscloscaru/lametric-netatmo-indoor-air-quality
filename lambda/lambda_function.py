import json
import urllib.parse, urllib.request
import os
from library import lnetatmo
from library import lametric

def lambda_handler(event, context):
    homeCoach = getHomeCoach()
    
    # Get metrics
    temp = homeCoach.getTemperature()
    humi = homeCoach.getHumidity()
    co2 = homeCoach.getCO2()
    
    # Get Icons
    tempIcon = getTempIcon(temp)
    humidityIcon = getHumidityIcon(humi)
    co2Icon = getCO2Icon(co2)
    
    # Lametric response helper
    lametric1 = lametric.Setup()
    lametric1.addTextFrame(tempIcon,str(temp) + "°")
    lametric1.addTextFrame(humidityIcon,str(humi) + "%")
    lametric1.addTextFrame(co2Icon,str(co2) + " ppm")
    response = lametric1.getData()
    
    return {
        'statusCode': 200,
        'body': json.dumps(response)
    }
    
def getHomeCoach(): 
    client_id = os.getenv('NETATMO_CLIENT_ID')
    client_secret = os.getenv('NETATMO_CLIENT_SECRET')
    username = os.getenv('NETATMO_USERNAME')
    password = os.getenv('NETATMO_PASSWORD')
    authorization = lnetatmo.ClientAuth(client_id, client_secret, username, password)
    return lnetatmo.HomeCoach(authorization)
 
# Icons definition
icon = {
    'temp_high': 'a13595', 
    'temp_low' : 'a13594', 
    'temp_ok' : 'a43248',
    'humi': 'i863', 
    'co2_ok': 'i4744',
    'co2_yellow': 'i43249',
    'co2_red': 'i43250'
    }

def getTempIcon(temp):
    temp_icon = icon['temp_ok']
    if temp < 22:
        temp_icon = icon['temp_low']
    if temp > 26:
        temp_icon = icon['temp_high']
    return temp_icon

def getHumidityIcon(humi):
    return icon['humi']
    
def getCO2Icon(co2):
    co2_icon = icon['co2_ok']
    if co2 > 1150:
        co2_icon = icon['co2_yellow']
    if co2 > 1600:
        co2_icon = icon['co2_red']
    return co2_icon
