"""
For a set of lights (see LIGHT_IDS), calculate the optimal colour temperature
(see color.py) for the time of day.

Then, set that colour temperature on every light that's in the list, if the light
is currently ON.

Needs hue_config.json to obtain API access info.

Call with -v to see what's going on.  Example output:

    ```
    Calculated colour temperature is 180 (daylite)

    2  - Sprudy               - on  - setting to 180... done
    6  - Kitchen lab light    - off - no action
    9  - Wall washer E        - off - no action
    11 - Kitchen fruitbowl    - off - no action
    12 - Wall washer N Lux    - off - no action
    13 - Wall washer W        - off - no action
    14 - Kitchen table        - off - no action
    15 - Kitchen fridge       - off - no action

    Finished.
    ```

To use as a cron job, put this sort of thing in crontab (remember end with a blank line)

7,17,27,37,47,57 * * * * /home/pi/daylite/.env/bin/python /home/pi/daylite/daylite_tweaker.py >> /dev/null

"""

LIGHT_IDS = [2, ] + [6, 9, 11, 12, 13, 14, 15]  # sprudy plus kitchen

from qhue.qhue import Bridge
from color import get_color
import json
import sys
import datetime
import logging
from pytz import UTC

verbose = '-v' in sys.argv
logging.basicConfig(level='WARNING' if verbose else 'ERROR', format="%(message)s")

# Load config. Contains username and other sensitive info.
with open("hue_config.json", "r") as f:
    config = json.loads(f.read())
    bridge = config["bridge"]

bridge = Bridge(bridge["address"], bridge["username"])

# What is optimum color temperature right now?
ct, explanation = get_color(datetime.datetime.now(tz=UTC))
logging.warning("\nCalculated colour temperature is %s (%s)\n", ct, explanation)

for light_id in LIGHT_IDS:
    light = bridge.lights[light_id]()

    name = light['name']
    state = 'on' if light['state']['on'] else 'off'
    
    # If the light is on and it has a 'ct' setting...
    if state == 'on':
        if 'ct' in light['state']:
            # ...set its colour temperature to daytime-optimal value
            action = 'setting to %d...' % ct
            bridge.lights[light_id].state(ct=ct)
            action += ' done'
        else:
            action = 'hue lux - no action'
    else:
        action = 'no action'

    logging.warning("%-2d - %-20s - %-3s - %s", light_id, name, state, action)

if verbose:
    sys.stdout.write("\nFinished.\n\n")
