"""Module to hold classes representing locations.

A location has latitude and longitude attributes to uniquely
identify itself.
"""

import re
import datetime


class FixedOffset(datetime.tzinfo):
    """Fixed offset in minutes east from UTC."""
    def __init__(self, offset):
        self.__offset = datetime.timedelta(hours=offset)

    def utcoffset(self, dt):
        return self.__offset

    def tzname(self, dt):
        return 'fixed'

    def dst(self, dt):
        return datetime.timedelta(0)


class Location(object):
  """Represents a location on a planet."""
  def __init__(self, latitude, longitude, name=None):
    """Creates a location instance."""
    self.__latitude = latitude
    self.__longitude = longitude
    self.__name = name
    self.__temperature = None
    self.__pressure = None
    self.__humidity = None
    self.__season = None
    self.__timezone = None
    self.__elevation = None

  def getCurrentTimeAsString(self):
    """Returns current local time at this location."""
    if self.__timezone is None:
      return str(self.__timezone)
    timedelta = float(self.__timezone.split('UTC')[1])
    dt = datetime.datetime.now(tz=FixedOffset(timedelta))
    return '%sT%sZ' % (dt.strftime('%Y-%m-%d'), dt.strftime('%T'))

  def getPosition(self):
    """Returns a comma separated latitude and longitude of this location."""
    return ','.join(str(l) for l in [self.latitude, self.longitude, self.elevation])

  def getTimezone(self):
    """Returns timezone at this location."""
    return self.__timezone

  def setTimezone(self, timezone):
    """Sets timezone at this location.

    The given timezone must be of the form 'UTC(+/-)<hours>'.
    For example, 'UTC+8.0' or 'UTC-2'
    """
    if not re.match(r'UTC[\+\-]\d+\.?\d*$', timezone):
      self.__timezone = 'UTC+0'
    else:
      self.__timezone = timezone
  
  def __str__(self):
    """Returns the location details in a way a planet's report() API expects."""
    attributes = [self.name, self.getPosition(),
                  self.getCurrentTimeAsString(),
                  self.season, self.getTemperatureAsString(),
                  self.getPressureAsString(), self.humidity]
    return '|'.join(str(p) for p in attributes)

  # Additional properties for the Location class.
  def getLatitude(self):
    return self.__latitude

  def getLongitude(self):
    return self.__longitude

  def getName(self):
    return self.__name
 
  def getTemperatureAsString(self):
    if self.__temperature:
      temperature = '%.1f' % self.__temperature
      if float(temperature) > 0:
        temperature = '+' + temperature
      return temperature
    return str(self.__temperature)

  def getTemperature(self):
    return self.__temperature

  def setTemperature(self, temperature):
    self.__temperature = temperature

  def getPressureAsString(self):
    if self.__pressure:
      return '%.1f' % self.__pressure
    return str(self.__pressure)

  def getPressure(self):
    return self.__pressure

  def setPressure(self, pressure):
    self.__pressure = pressure

  def getHumidity(self):
    return self.__humidity

  def setHumidity(self, humidity):
    self.__humidity = humidity

  def getElevation(self):
    return self.__elevation

  def setElevation(self, elevation):
    self.__elevation = elevation

  def getSeason(self):
    return self.__season

  def setSeason(self, season):
    if season == 'summer':
      self.__season = 'Sunny'
    elif season == 'winter':
      self.__season = 'Snow'
    elif season == 'rain':
      self.__season = 'Rain'
    else:
      self.__season = season

  latitude = property(getLatitude)
  longitude = property(getLongitude)
  name = property(getName)
  temperature = property(getTemperature, setTemperature)
  pressure = property(getPressure, setPressure)
  humidity = property(getHumidity, setHumidity)
  season = property(getSeason, setSeason)
  timezone = property(getTimezone, setTimezone)
  elevation = property(getElevation, setElevation)
