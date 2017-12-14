"""Module to hold different types of weather controllers for planets.

Every weather controller is a thread that is responsible to update
climatic conditions on a set of planets it is controlling. Typically,
a weather change happens at a fixed interval.

This module also has an astract base class that serves as a decorator
for the base weather controller. A series of decorators can be added
on top of a base weather. For example, for a periodic base weather
one can add decortors like rain, hurricane, thunderstorm etc.

As well contains a Factory Method "createWeatherController" to create a
weather controller instance based in the base_weather and weather_decorators
values in the all_data.json file for a planet.
"""

import os
import sys

import collections
import random
import threading
import time

from abc import ABCMeta
from abc import abstractmethod


# A constant holding the range of longitudes on a planet.
_LONGITUDE_RANGE = (-179.999, 180)


class Controller(threading.Thread):
  """The base class for a weather controller."""
  def __init__(self):
    super(Controller, self).__init__()
    # The set of planets this thread will control weather on.
    self._planets = set([])
    # A boolean flag used to stop the controller thread.
    self._should_run = True

  def addPlanet(self, planet):
    self._planets.add(planet)

  def getPlanets(self):
    return self._planets

  def shutdown(self):
    """Turns this controller thread off at program termination."""
    self._should_run = False


class PeriodicController(Controller):
  """A concrete weather controller that has periodic season changes.

  A planet with periodic seasons must mention a 'revolution_period'
  in all_data.json. This thread keeps a counter and once it reaches
  the stage where the planet has completed half revolution around its
  parent star, the seasons are changed.
  """
  def __init__(self):
    super(PeriodicController, self).__init__()
    # A dict mapping a planet to current seasons on its zones.
    self._planet_season_clock = {}

  def run(self):
    for planet in self._planets:
      # Initialize the clock for season change.
      self._planet_season_clock[planet] = 0
    while self._should_run:
      for planet, season_clock in self._planet_season_clock.items():
        # Half revolution around the parent star triggers season change.
        planet_period = data_reader.GetPeriod(planet) / 2
        new_clock = (season_clock + 1) % planet_period
        self._planet_season_clock[planet] = new_clock
        if new_clock == 0:
          # We have circled half around the parent star.
          # Now is the time to switch seasons.
          with planet.season_change_lock:
            # Switch seasons.
            temp_zone = planet.summer_zones
            planet.summer_zones = planet.winter_zones
            planet.winter_zones = temp_zone
        time.sleep(3)


class WeatherControllerDecorator(Controller):
  """An abstract base class for weather decorators.

  This is a decorator for the Controller class.
  Each subclass of this class induces a certain
  temporary weather condition on a planet. Examples
  are Rain, Wind, Hurricane, Tsunami etc. 
  """
  __metaclass__ = ABCMeta

  def __init__(self, controller):
    super(WeatherControllerDecorator, self).__init__()
    self._base_controller = controller
    self._data_loaded = threading.Event()

  def addPlanet(self, planet):
    """Adds a planet to this decorator."""
    self._base_controller.addPlanet(planet)
    self._planets.add(planet)
    planet.addWeatherDecorator(self)

  def shutdown(self):
    """The function to stop this controller thread at program termination."""
    self._base_controller.shutdown()
    self._should_run = False

  @abstractmethod
  def getPlanetData(self):
    pass


class RainController(WeatherControllerDecorator):
  """An instance of weather decorator to induce rain on a planet.

  Reads the "rain_zones" entry from all_data.json to determine
  allowed locations where it can rain on a planet. The thread
  then starts rain on randomly selected regions on the planet.
  The regions are always within the allowed rain_zones.
  """
  def __init__(self, weathercontroller):
    super(RainController, self).__init__(weathercontroller)
    self._planet_rain_locations = collections.defaultdict(tuple)
    
  def getPlanetData(self, planet):
    """The function that tells a planet where it is raining currently.

    This is needed while the planet is generating its report. 
    """
    planet_data = self._planet_rain_locations.get(planet, [])
    if planet_data:
      planet_lock = planet_data[0]
      rain_locations = []
      with planet_lock:
        rain_locations = planet_data[1]
      return rain_locations
    return planet_data

  def run(self):
    # Start the other decorator, if any.
    self._base_controller.start()
    while self._should_run:
      for planet in self._planets:
        # Get allowed rain latitudes to not rain on a disallowed region.
        min_latitude, max_latitude = getAllowedRainLatitudes(planet)
        planet_data = self._planet_rain_locations[planet]
        # Acquire the data writer lock. If the lock does not exist,
        # create a new lock that will be later made avaialable to readers.
        if planet_data:
          planet_lock = planet_data[0]
        else:
          planet_lock = threading.Lock()
        new_rain_locations = []
        count_rain_regions = random.randint(1, 10)
        for _ in range(count_rain_regions):
          start_latitude = random.uniform(min_latitude, max_latitude)
          start_longitude = random.uniform(*_LONGITUDE_RANGE)
          end_latitude = random.uniform(min_latitude, max_latitude)
          end_longitude = random.uniform(*_LONGITUDE_RANGE)
          start_location = Location(latitude=start_latitude, longitude=start_longitude)
          end_location = Location(latitude=end_latitude, longitude=end_longitude)
          # Arrange co-ordinates of the chosen region to view it as a rectangular region.
          new_rain_locations.append(arrange(start_location, end_location))
        with planet_lock: 
          self._planet_rain_locations[planet] = (planet_lock, new_rain_locations)
      time.sleep(3)


def arrange(location_a, location_b):
  """Arranges the coordinates of two locations to represent it as a rectangular region.

  Given two locations, this function returns the lower-left and top-right coordinates
  of the rectangular region formed by them. 
  """
  if location_a.latitude < location_b.latitude:
    if location_b.longitude < location_a.longitude:
      ret_tuple = (Location(latitude=location_a.latitude, longitude=location_b.longitude),
                   Location(latitude=location_b.latitude, longitude=location_a.longitude))
      return ret_tuple
    else:
      return (location_a, location_b)
  elif location_a.latitude == location_b.latitude:
    if location_b.longitude < location_a.longitude:
      ret_tuple = (Location(latitude=location_a.latitude, longitude=location_b.longitude),
                   Location(latitude=location_b.latitude, longitude=location_a.longitude))
      return ret_tuple
    else:
      return (location_a, location_b)
  else:  # i.e. location_a.latitude > location_b.latitude:
    if location_a.longitude < location_b.longitude:
      ret_tuple = (Location(latitude=location_b.latitude, longitude=location_a.longitude),
                   Location(latitude=location_a.latitude, longitude=location_b.longitude))
      return ret_tuple
    else:
      return (location_b, location_a)
    

def getAllowedRainLatitudes(planet):
  """Reads the rain_zones for a planet as mentioned in all_data.json file.

  Returns a tuple of the minimum and maximum latitudes within which it is 
  allowed to rain on a planet.
  """
  planet_data = data_reader.GetPlanetData(planet)
  rain_zones = data_reader.GetRainZones(planet)
  all_zones = planet_data['zones']
  zone_data = {k: all_zones[k] for k in all_zones if k in rain_zones}
  regions = [latitude for zone in zone_data.values() for latitude in zone]
  return min(regions), max(regions)


def createWeatherController(base_weather, weather_decorators):
  """Factory method to create an instance of a weather controller.

  The base_weather and the weather_decorators entries for a planet
  in the all_data.json file helps decide what concrete instance to
  create.
  """
  def createBaseController(base_weather):
    if base_weather == 'periodic':
      return PeriodicController()

  def createWeatherDecorator(decorator, base_controller):
    if decorator == 'rain':
      return RainController(base_controller)

  weather_controller = createBaseController(base_weather)
  for decorator_name in weather_decorators:
    weather_controller = createWeatherDecorator(decorator_name, weather_controller)
  return weather_controller

if __name__ != '__main__':
  # This module is being imported.
  project_path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
  if project_path not in sys.path:
    sys.path.append(project_path)
  from data_reader import data_reader
  from location.location import Location

