"""Module to hold classes representing different planet types.

Contains an abstract base type Planet and its concrete sub-classes.

As well contains a Factory Method "createPlanet" to create a
Planet instance based on its base-weather in the all_data.json file.
"""
import os
import random
import sys
import threading
import time

from abc import ABCMeta
from abc import abstractmethod


class Planet(object):
  """An abstract base class for planets."""
  __metaclass__ = ABCMeta

  def __init__(self, planet_data):
    self._name = planet_data['name']
    self._revolution_period = planet_data['revolution_period']
    self._locations = set([])
    self._weather_decorators = []
    for location_data in planet_data['locations']:
      location = Location(
          latitude=location_data['latitude'],
          longitude=location_data['longitude'],
          name= location_data['name'])
      location.timezone = location_data['timezone']
      location.elevation = location_data['elevation']
      self._locations.add(location)

  def getName(self):
    return self._name

  def addWeatherDecorator(self, weather_decorator):
    """Adds a weather decorator (rain, wind, hurricane, etc.)"""
    self._weather_decorators.append(weather_decorator)

  def getWeatherDecorators(self):
    """Returns the list of weather decorators chosen for this planet."""
    return self._weather_decorators

  def getLocations(self):
    """Returns a list of locations on this planet.

    The locations are sorted by longitude i.e. east to west.
    """
    return reversed(sorted(self._locations, key=lambda l: l.longitude))

  def __hash__(self):
    return self._name.__hash__()

  def __eq__(self, other):
    return self._name == other._name

  @abstractmethod
  def report(self):
    pass

  name = property(fget=lambda self: self.getName())


class PeriodicWeatherPlanet(Planet):
  """Represents planets that have a periodic weather transition.

     An example is Earth that has transitioning seasons
     (summer and winter) after a fixed period of 6 months.
  """
  def __init__(self, planet_data):
    """Creates a PeriodicWeatherPlanet instance."""
    super(PeriodicWeatherPlanet, self).__init__(planet_data)
    all_zones = sorted(planet_data['zones'].keys())
    mid = len(all_zones) / 2
    # Half of the total zones are having summer season.
    self._summer_zones = all_zones[:mid]
    # The other half has winter.
    self._winter_zones = all_zones[mid:]
    # The weather controller thread switches seasons at regular intervals.
    self._season_change_lock = threading.Lock()

  def report(self):
    """Prints to STDOUT current weather conditions on this planet.

    The report contains locations mentioned in the all_data.json file.
    """
    decorated_locations = [l for d in self.getWeatherDecorators() for l in d.getPlanetData(self)]
    for location in self.getLocations():
      zone = data_reader.GetZone(location, self)
      for region in decorated_locations:
        # Check if the current location has been decorated with rain.
        if (region[0].latitude <= location.latitude <= region[1].latitude) and (
            region[0].longitude <= location.longitude <= region[1].longitude):
          season = 'rain'
          break
      else:
        # If its not raining then its either snowy or sunny.
        if zone in self._summer_zones:
          season = 'summer'
        else:
          season = 'winter'
      # Set the current temperature, pressure and humidity as per
      # the allowed range in the all_data.json file.
      location.temperature = random.uniform(*data_reader.GetTemperatureRange(self, zone, season))
      location.pressure = random.uniform(*data_reader.GetPressureRange(self, zone, season))
      location.humidity = random.randint(*data_reader.GetHumidityRange(self, zone, season))
      location.season = season
      print location
    print os.linesep    

  def getSummerZones(self):
    return self._summer_zones

  def setSummerZones(self, zones):
    self._summer_zones = zones

  def getWinterZones(self):
    return self._winter_zones

  def setWinterZones(self, zones):
    self._winter_zones = zones

  def getSeasonChangeLock(self):
    return self._season_change_lock

  summer_zones = property(fget=lambda self: self.getSummerZones(), fset=lambda self, summer_zones: self.setSummerZones(summer_zones))
  winter_zones = property(fget=lambda self: self.getWinterZones(), fset=lambda self, winter_zones: self.setWinterZones(winter_zones))
  season_change_lock = property(fget=lambda self: self.getSeasonChangeLock())


def createPlanet(planet_data):
  """A factory method to create a planet.

  The base_weather mentioned in the all_data.json file
  decides what kind of planet instance is returned.
  """
  base_weather = planet_data.get('base_weather')
  if 'periodic' == base_weather:
    return PeriodicWeatherPlanet(planet_data)


if __name__ != '__main__':
  # This module is being imported.
  project_path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
  if project_path not in sys.path:
    sys.path.append(project_path)
  from data_reader import data_reader
  from location.location import Location

