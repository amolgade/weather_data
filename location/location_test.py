"""The unit test module for location.

Covers unit tests for functions in the Location class.
"""

import unittest
from location import Location


class LocationUnitTester(unittest.TestCase):
  """Tests properties and APIs in the location.Location class."""

  def test_getPosition(self):
    test_location = Location(latitude=0, longitude=0.0)
    self.assertEqual(test_location.getPosition(), '0,0.0')

  def test_property_latitude(self):
    test_location = Location(latitude=80.0, longitude=0.0)
    self.assertEqual(test_location.latitude, 80.0)

  def test_property_longitude(self):
    test_location = Location(latitude=80.0, longitude=0.0)
    self.assertEqual(test_location.longitude, 0.0)

  def test_property_temperature(self):
    test_location = Location(latitude=0.0, longitude=0.0)
    self.assertIsNone(test_location.temperature)
    test_location.temperature = 40
    self.assertEqual(test_location.temperature, 40)

  def test_string_output(self):
    """Tests the output of an str() call on a location."""
    def mock_current_time():
      return 'YYYY-DD-MM'
    test_location = Location(latitude=0.0, longitude=0.0, name='test_location')
    test_location.getCurrentTimeAsString = mock_current_time
    self.assertEqual(str(test_location), 'test_location|0.0,0.0|None|None|None|None|YYYY-DD-MM')


if __name__ == '__main__':
  unittest.main()
