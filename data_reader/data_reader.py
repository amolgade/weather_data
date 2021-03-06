"""
Module to have classes that read data from all_data.json file.

These classes have APIs to query for required data.
"""
import json
import os
import threading
import time


# A global instance of the DataReader class.
# DataReader is a singleton class.
_DATA_READER = None

# A global lock to instantiate the singleton DataReader.
_SINGLETON_LOCK = threading.Lock()

# An event that the DataReader thread has started.
_DATA_READER_STARTED = threading.Event()

# An event that the DataReader thread is shutdown.
_DATA_READER_SHUTDOWN = threading.Event()


class DataReaderError(Exception):
  """Base Error to raise in case of exceptions."""
  pass


class DataReader(threading.Thread):
  """Singleton class that reads data from all_data.json file.

  A DataReader instance runs as a thread.
  """
  def __init__(self, data_source, data_refresh_interval_seconds=2):
    super(DataReader, self).__init__()
    self.__source = data_source
    self.__refresh_rate = data_refresh_interval_seconds
    self.__data = None
    self.__data_lock = threading.Lock()
    self.__should_read = True

  def run(self):
    while True:
      if self.__should_read:
        _DATA_READER_SHUTDOWN.clear()
        try:
          with open(self.__source) as fp:
            with self.__data_lock:
              self.__data = json.load(fp)
        except IOError as e:
          self.__should_read = False
          raise DataReaderError('Cannot load data from %s: Error: %s' % (self.__source, e))
        finally:
          _DATA_READER_STARTED.set()
        time.sleep(self.__refresh_rate)
      else:
        _DATA_READER_SHUTDOWN.set()
        return 

  def GetAllData(self):
    """Returns all data from the all_data.json file."""
    all_data = None
    with self.__data_lock:
      all_data = self.__data
    return all_data

  def close(self):
    """Sets self.__should_read to Flase to stop the thread."""
    self.__should_read = False


def shutdown():
  """Shuts the DataReader thread down and sets the shutdown event."""
  global _DATA_READER
  if _DATA_READER is not None:
    _DATA_READER.close()
    _DATA_READER_SHUTDOWN.wait()

# Below are the APIs that this module provides to fetch data from all_data.json.
def GetAllData():
  """Returns entire data in all_data.json file."""
  global _DATA_READER, _SINGLETON_LOCK
  with _SINGLETON_LOCK:
    if _DATA_READER is None:
      _DATA_READER = DataReader(os.path.join(os.path.dirname(__file__), 'all_data.json'))
      _DATA_READER.start()
      _DATA_READER_STARTED.wait()
  return _DATA_READER.GetAllData()

def GetPlanetData(planet):
  """Returns all data in the all_data.json for a given planet.

  Raises DataError is not data is found.
  """
  all_data = GetAllData()
  for planet_data in all_data.get('planets'):
    if planet_data.get('name') == planet.name:
      return planet_data
  else:
     raise DataReaderError('No data found for: %s' % planet.name)

def GetPeriod(planet):
  """Returns the given planet's revolution period as mentioned in the all_data.json file."""
  planet_data = GetPlanetData(planet)
  return planet_data.get('revolution_period', 12)

def GetRainZones(planet):
  """Returns valid regions it can rain for a given planet from all_data.json file."""
  planet_data = GetPlanetData(planet)
  return planet_data.get('rain_zones', [])

def GetTemperatureRange(planet, zone, season):
  """Returns temperature range for a given planet, zone and season from all_data.json file."""
  planet_data = GetPlanetData(planet)
  zone_info = planet_data.get('zone_data', {}).get(zone, {})
  temperature_range = zone_info.get(season, {}).get('temperature')
  return tuple(temperature_range)

def GetPressureRange(planet, zone, season):
  """Returns pressure range for a given planet, zone and season from all_data.json file."""
  planet_data = GetPlanetData(planet)
  zone_info = planet_data.get('zone_data', {}).get(zone, {})
  pressure_range = zone_info.get(season, {}).get('pressure')
  return tuple(pressure_range)

def GetHumidityRange(planet, zone, season):
  """Returns humidity range for a given planet, zone and season from all_data.json file."""
  planet_data = GetPlanetData(planet)
  zone_info = planet_data.get('zone_data', {}).get(zone, {})
  humidity_range = zone_info.get(season, {}).get('humidity')
  return tuple(humidity_range)

def GetZone(location, planet):
  """Returns the zone the given location is on a planet.

  Raises DataError if the zone cannot be determined.
  """
  planet_data = GetPlanetData(planet)
  zones = planet_data.get('zones', {})
  if location.latitude >= 0:
    for zone_name, zone_range in zones.iteritems():
      if zone_range[0] <= location.latitude <= zone_range[1]:
        return zone_name
    else:
      raise DataReaderError('Cannot determine zone for location: %s', location)
  else:
    for zone_name, zone_range in zones.iteritems():
      if zone_range[0] >= location.latitude >= zone_range[1]:
        return zone_name
    else:
      raise DataReaderError('Cannot determine zone for location: %s', location)
  
