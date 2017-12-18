"""This module prints weather report on STDOUT a given number of times every 6 seconds.

The file all_data.json captures all data required to run this weather simulation.

The planet_loader module yields planet objects as mentioned in all_data.json file.
A planet object has a report() function to print its current weather conditions
on a fixed set of locations. The output weather conditions differ with each call
to the planet.report() function.


Invoke this module as:-
python WeatherGenerator.py
This will result in getting current weather data displayed 20 times by default.

To display weather data 50 times, invoke this module as:-
python WeatherGenerator.py 50
"""
import sys
import time

def _main(arg):
  print __doc__
  print 'To continue, hit <Enter>'
  raw_input()
  try:
   for planet in planet_loader.getAllPlanets():
     for _ in range(times):
       # Generate weather report and sleep for 6 seconds before continuing.
       planet.report()
       time.sleep(6)  # seconds.
  finally:
    planet_loader.close()


if __name__ == '__main__':
  times = sys.argv[1] if len(sys.argv) > 1 else 20
  try:
    times = int(times)
  except (ValueError, TypeError):
    print 'Invalid argument \'%s\'. Please specify a number.' % sys.argv[1]
  else:
    from planets import planet_loader
    _main(times)
