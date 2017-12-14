"""Module to load all planets from all_data.json.

This is a helper module to the main module that runs
weather simulation.

This module is also responsible for starting weather controllers
and data reader threads and closing then on program termination.
"""

import os
import sys

import planets


# A global list of all weather controller threads.
_WEATHER_CONTROLLERS = []


def getAllPlanets():
  """A generator to create and yield a planet.
  
  All data required to create a planet object comes from the all_data.json file.
  """
  # Load entire all_data.json.
  all_data = data_reader.GetAllData()
  for planet_data in all_data['planets']:
    # Create planets and weather controller objects.
    # These are created using their respective factory methods.
    planet = planets.createPlanet(planet_data)
    weather_controller = controllers.createWeatherController(
        planet_data['base_weather'], planet_data['weather_decorators'])
    weather_controller.addPlanet(planet)
    weather_controller.start()
    _WEATHER_CONTROLLERS.append(weather_controller)
    yield planet


def close():
  """Shuts all background thread down before program termination."""
  data_reader.shutdown()
  for controller in _WEATHER_CONTROLLERS:
    controller.shutdown()

if __name__ != '__main__':
  project_path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
  if project_path not in sys.path:
    sys.path.append(project_path)
  from controllers import controllers
  from data_reader import data_reader
  from location import location
