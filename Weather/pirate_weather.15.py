#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# <xbar.title>Pirate Weather</xbar.title>
# <xbar.version>v1.0</xbar.version>
# <xbar.author>Daniel Seripap, Valerio, pca2</xbar.author>
# <xbar.author.github>seripap, scartiloffista, pca2</xbar.author.github>
# <xbar.desc>Detailed weather plugin powered by PirateWeather.net with auto location lookup. Fork of original DarkSky-based script with drop-in replacement API pirateweater.net instead. Supports metric and imperial units. Needs API key from https://pirateweater.net/getting-started.</xbar.desc>
# <xbar.image>https://cloud.githubusercontent.com/assets/683200/16276583/ff267f36-387c-11e6-9fd0-fc57b459e967.png</xbar.image>
# <xbar.dependencies>python</xbar.dependencies>


# -----------------------------------------------------------------------------------
# For a more accurate location lookup, download and install CoreLocationCLI
# Available here: https://github.com/fulldecent/corelocationcli/releases
# This will allow a more precise location lookup as it uses native API for loc lookup
# -----------------------------------------------------------------------------------

import json
import urllib.request, urllib.error, urllib.parse
import textwrap
from random import randint
import subprocess

# get yours at https://pirateweather.net/
api_key = ''

# get yours API key for encode location at https://opencagedata.com
geo_api_key = ''

# if you want to set manual location, define following two vars. If left empty, script will try to determine the location
# example:
manual_city = ''
manual_latlng = ''
# manual_city = 'Paris'
# manual_latlng = '48.8566,2.3522'


# set to si for metric, leave blank for imperial
units = 'si'

# optional, see message above
core_location_cli_path = '~/CoreLocationCLI'

def manual_location_lookup():
  if manual_latlng == "" or manual_city == "":
     return False;
  else:
     return { "loc": manual_latlng, "preformatted": manual_city }

def mac_location_lookup():
  try:
    exit_code, loc = subprocess.getstatusoutput(core_location_cli_path + ' -once -format "%latitude,%longitude"')
    if exit_code != 0:
      raise ValueError('CoreLocationCLI not found')
    formatted_city_name = reverse_latlong_lookup(loc)
    return { "loc": loc, "preformatted": formatted_city_name }
  except:
    return False

def auto_loc_lookup():
  try:
    location = urllib.request.urlopen('https://ipinfo.io/json')
    return json.load(location)
  except urllib.error.URLError:
    return False

def reverse_latlong_lookup(loc):
  try:
    location_url = 'https://api.opencagedata.com/geocode/v1/json?q=' + loc + '&key=' + geo_api_key + '&language=en&pretty=1'
    location = json.load(urllib.request.urlopen(location_url))
    if 'results' in location:
      return location['results'][0]['formatted']
    else:
      return 'Could not lookup location name'
  except:
    return 'Could not lookup location name'

def full_country_name(country):
  try:
    countries = json.load(urllib.request.urlopen('http://country.io/names.json'))
    try:
      if country in countries:
        return countries[country]
      else:
        return False
    except KeyError:
      return False
  except urllib.error.URLError:
    return False

def calculate_bearing(d):
  dirs = ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE', 'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW']
  ix = int(round(d / (360. / len(dirs))))
  return dirs[ix % len(dirs)]

def get_wx_icon(icon_code):
  if icon_code == 'clear-day':
    icon = "☀️"
  elif icon_code == 'clear-night':
    icon = "🌙"
  elif icon_code == 'rain':
    icon = "🌧️"
  elif icon_code == 'snow':
    icon = "❄️"
  elif icon_code == 'sleet':
    icon = "🌨️"
  elif icon_code == 'wind':
    icon = "💨"
  elif icon_code == 'fog':
    icon = "🌫️"
  elif icon_code == 'cloudy':
    icon = "☁️"
  elif icon_code == 'partly-cloudy-day':
    icon = "🌤️"
  elif icon_code == 'partly-cloudy-night':
    icon = "☁️"
  else:
    icon = ''

  return icon

def get_wx():

  if api_key == "":
    return False

  location = manual_location_lookup() or mac_location_lookup() or auto_loc_lookup()

  if location is False:
    return False

  for locData in location:
    locData

  try:
    if 'loc' in location:
      wx = json.load(urllib.request.urlopen('https://api.pirateweather.net/forecast/' + api_key + '/' + location['loc'] + '?units=' + units + "&v=" + str(randint(0,100))))
    else:
      return False
  except urllib.error.HTTPError:
    return False

  if units == 'si':
    unit = 'C'
    distance = 'm/s'
    distance_short = 'km'
  else:
    unit = 'F'
    distance = 'mph'
    distance_short = 'mi'

  try:

    weather_data = {}

    if 'currently' in wx:
      for item in wx['currently']:
        if item == 'temperature':
          weather_data['temperature'] = str(int(round(wx['currently']['temperature']))) + '°' + unit
        elif item == 'icon':
          weather_data['icon'] = get_wx_icon(str(wx['currently']['icon']))
        elif item == 'summary':
          weather_data['condition'] = str(wx['currently']['summary'])
        elif item == 'windSpeed':
          weather_data['wind'] = str(wx['currently']['windSpeed']) + ' ' + distance
        elif item == 'windBearing':
          weather_data['windBearing'] = calculate_bearing(wx['currently']['windBearing'])
        elif item == 'humidity':
          weather_data['humidity'] = str(int(round(wx['currently']['humidity'] * 100))) + '%'
        elif item == 'dewPoint':
          weather_data['dewPoint'] = str(wx['currently']['dewPoint'])
        elif item == 'visibility':
          weather_data['visibility'] = str(int(round(wx['currently']['visibility']))) + ' ' + distance_short
        elif item == 'pressure':
          weather_data['pressure'] = str(wx['currently']['pressure']) + ' mb'
        elif item == 'apparentTemperature':
          weather_data['feels_like'] = str(int(round(wx['currently']['apparentTemperature']))) + '°' + unit

    if 'minutely' in wx:
      for item in wx['minutely']:
        if item == 'summary':
          weather_data['next_hour'] = str((wx['minutely']['summary']))

    if 'daily' in wx:
      for item in wx['daily']:
        if item == 'summary':
          weather_data['week'] = str((wx['daily']['summary']))

    if 'city' in location and 'region' in location:
      if location['city'] == '' and location['region'] == '':
        if 'country' in location:
            country = full_country_name(location['country'])

            if country is False or location['country'] == '':
              weather_data['country'] = 'See Full Forecast'
            else:
              weather_data['country'] = country
      else:
        weather_data['city'] = str(location['city'])
        weather_data['region'] = str(location['region'])

    if 'loc' in location:
      weather_data['loc'] = str(location['loc'])

    if 'preformatted' in location:
      weather_data['preformatted'] = location['preformatted']

  except KeyError:
    return False

  return weather_data

def render_wx():

  if api_key == '':
    print('Missing API key')
    print('---')
    print('Get an API Key | href=https://pirateweather.net/getting-started')
    return False

  weather_data = get_wx()

  if weather_data is False:
    print('--')
    print('---')
    print('Could not get weather data at this time')
    return False

  if 'icon' in weather_data and 'temperature' in weather_data:
    print(weather_data['icon'] + " " + weather_data['temperature'] + "| emojize=true")
  else:
    print('N/A')

  print('---')


  if 'city' in weather_data and 'region' in weather_data:
    print(weather_data['city'] + ', ' + weather_data['region'] + ' | href=https://merrysky.net/forecast/' + weather_data['loc'] + '?units=' + units )
  elif 'country' in weather_data:
    print(weather_data['country'] + ' | href=https://merrysky.net/forecast/' + weather_data['loc'] + '?units=' + units )
  elif 'preformatted' in weather_data:
    print(weather_data['preformatted'] + ' | href=https://merrysky.net/forecast/' + weather_data['loc'] + '?units=' + units )

  if 'condition' in weather_data and 'feels_like' in weather_data:
    print(weather_data['condition'] + ', Feels Like: ' + weather_data['feels_like'])

  print('---')

  if 'next_hour' in weather_data:
    print("Next hour: " + weather_data['next_hour'])
    print('---')
  else:
    print('---')

  if 'week' in weather_data:
    print("\n".join(textwrap.wrap(weather_data['week'], 50)))
    print('---')

  if 'wind' in weather_data and 'windBearing' in weather_data:
    print('Wind: ' + weather_data['wind'] + ' ' + weather_data['windBearing'])

  if 'humidity' in weather_data:
    print('Humidity: ' + weather_data['humidity'])

  if 'dewPoint' in weather_data:
    print('Dew Point: ' + weather_data['dewPoint'])

  if 'visibility' in weather_data:
    print('Visibility: ' + weather_data['visibility'])

  if 'pressure' in weather_data:
    print('Pressure: ' + weather_data['pressure'])

  print('---')
  print('Powered by PirateWeather | href=https://pirateweather.net/')

render_wx()
