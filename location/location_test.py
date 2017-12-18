"""The unit test module for location.

Covers unit tests for functions and properties in the Location class.
"""
import re
import unittest

from location import Location


class LocationUnitTester(unittest.TestCase):
  """Tests properties and APIs in the location.Location class."""

  def setUp(self):
    """Setup data/environment for a test before running it."""
    self._test_location = Location(latitude=0, longitude=0.0)
    
  def test_property_season(self):
    self.assertIsNone(self._test_location.season)
    self._test_location.season = 'summer'
    self.assertEqual(self._test_location.season, 'Sunny')
    self._test_location.season = 'winter'
    self.assertEqual(self._test_location.season, 'Snow')
    self._test_location.season = 'rain'
    self.assertEqual(self._test_location.season, 'Rain')
    self._test_location.season = 'Windy'
    self.assertEqual(self._test_location.season, 'Windy')

  def test_property_temperature(self):
    self.assertIsNone(self._test_location.temperature)
    self._test_location.temperature = 40
    self.assertEqual(self._test_location.temperature, 40)
    self._test_location.temperature = -40
    self.assertEqual(self._test_location.temperature, -40)
    self._test_location.temperature = 40.5
    self.assertEqual(self._test_location.temperature, 40.5)
    self._test_location.temperature = -40.5
    self.assertEqual(self._test_location.temperature, -40.5)
    self._test_location.temperature = 40.56789
    self.assertEqual(self._test_location.temperature, 40.56789)
    self._test_location.temperature = -40.56789
    self.assertEqual(self._test_location.temperature, -40.56789)

  def test_GetTemperatureAsString(self):
    self.assertEqual(self._test_location.getTemperatureAsString(), 'None')
    self._test_location.temperature = 40
    self.assertEqual(self._test_location.getTemperatureAsString(), '+40.0')
    self._test_location.temperature = -40
    self.assertEqual(self._test_location.getTemperatureAsString(), '-40.0')
    self._test_location.temperature = 40.5
    self.assertEqual(self._test_location.getTemperatureAsString(), '+40.5')
    self._test_location.temperature = -40.5
    self.assertEqual(self._test_location.getTemperatureAsString(), '-40.5')
    self._test_location.temperature = 40.56789
    self.assertEqual(self._test_location.getTemperatureAsString(), '+40.6')
    self._test_location.temperature = -40.56789
    self.assertEqual(self._test_location.getTemperatureAsString(), '-40.6')

  def test_property_pressure(self):
    self.assertIsNone(self._test_location.pressure)
    self._test_location.pressure = 1040
    self.assertEqual(self._test_location.pressure, 1040)
    self._test_location.pressure = 1040.5
    self.assertEqual(self._test_location.pressure, 1040.5)
    self._test_location.pressure = 1040.56789
    self.assertEqual(self._test_location.pressure, 1040.56789)

  def test_GetPressureAsString(self):
    self.assertEqual(self._test_location.getPressureAsString(), 'None')
    self._test_location.pressure = 1040
    self.assertEqual(self._test_location.getPressureAsString(), '1040.0')
    self._test_location.pressure = 1040.5
    self.assertEqual(self._test_location.getPressureAsString(), '1040.5')
    self._test_location.pressure = 1040.56789
    self.assertEqual(self._test_location.getPressureAsString(), '1040.6')

  def test_getPosition(self):
    self.assertEqual(self._test_location.getPosition(), '0,0.0,None')
    self._test_location.elevation = 50
    self.assertEqual(self._test_location.getPosition(), '0,0.0,50')

  def test_property_latitude(self):
    test_location = Location(latitude=80.0, longitude=0.0)
    self.assertEqual(test_location.latitude, 80.0)

  def test_property_longitude(self):
    test_location = Location(latitude=80.0, longitude=0.0)
    self.assertEqual(test_location.longitude, 0.0)

  def test_GetCurrentTimeAsString(self):
    time_regex = r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$'
    self.assertEqual(self._test_location.getCurrentTimeAsString(), 'None')
    self._test_location.timezone = 'UTC+8'
    self.assertTrue(re.match(time_regex, self._test_location.getCurrentTimeAsString()))
    self._test_location.timezone = 'UTC-10'
    self.assertTrue(re.match(time_regex, self._test_location.getCurrentTimeAsString()))
    self._test_location.timezone = 'Invalid_time_zone'
    self.assertTrue(re.match(time_regex, self._test_location.getCurrentTimeAsString()))
    
  def test_string_output(self):
    """Tests the output of an str() call on a location."""
    def mock_current_time():
      return 'YYYY-DD-MM'
    test_location = Location(latitude=0.0, longitude=0.0, name='test_location')
    test_location.getCurrentTimeAsString = mock_current_time
    test_location.temperature = 100
    test_location.pressure = 1000
    test_location.humidity = 4
    self.assertEqual(str(test_location), 'test_location|0.0,0.0,None|YYYY-DD-MM|None|+100.0|1000.0|4')


if __name__ == '__main__':
  unittest.main()
