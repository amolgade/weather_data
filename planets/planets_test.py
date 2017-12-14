"""The unit test module for planets.py.

Covers unit tests for factory methods in the planets module.
"""

import copy
import os
import sys
import unittest
import planets


_TEST_PLANET_DATA = {
      "name": "test_planet",
      "base_weather": "periodic",
      "weather_decorators":  ["storm"],
      "zones": {
        "Z1": [-90, 90]
      },
      "zone_data": {
        "Z1": {
          "summer": {"temperature": [35, 50], "pressure": [1000, 1200], "humidity": [10, 20]},
          "winter": {"temperature": [20, 40], "pressure": [900, 1050], "humidity": [12, 25]},
          "rain": {"temperature": [15, 30], "pressure": [1000, 1200], "humidity": [70, 85]}
        }
      },
      "revolution_period": 3,
      "locations": [
        {
          "name": "test_location",
          "latitude": 51.36,
          "longitude": -0.7,
          "timezone": "UTC+1",
          "elevation": 35
        }
      ]
}


class PlanetFactoryMethodTester(unittest.TestCase):
  """Tests factory methods in the planets module."""
  def setUp(self):
    """Setup test data before running a test."""
    self._test_data = copy.deepcopy(_TEST_PLANET_DATA)

  def testCreatePlanetReturnsNone(self):
    """Tests no planet is created if the base_weather is invalid."""
    self._test_data['base_weather'] = 'invalid_weather_descriptor'
    self.assertIsNone(planets.createPlanet(self._test_data))

  def testCreatePlanet(self):
    """Tests correct planet sub-class is instantiated based on the base_weather."""
    self.assertIsInstance(planets.createPlanet(self._test_data), planets.PeriodicWeatherPlanet)


if __name__ == '__main__':
  unittest.main()

