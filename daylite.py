from qhue.qhue import Bridge
from color import get_color
import json
import datetime
import requests
from pytz import UTC

# Load config. Contains username and other sensitive info.
with open("hue_config.json", "r") as f:
    config = json.loads(f.read())
    bridge = config["bridge"]

bridge = Bridge(bridge["address"], bridge["username"])

# What is optimum color temperature right now?
auto = {}
auto["ct"], explanation = get_color(datetime.datetime.now(tz=UTC))

scene_id = config["scene_id"]
rule_id  = config["rule_id"]

# Set lights for scene if necessary
if not sorted(bridge.scenes[scene_id]()['lights']) == sorted(config['lights'].keys()):
  bridge.scenes[scene_id](name='daylite',lights=config['lights'].keys())

# Mod lightstates for specified scene
for light_id in config["lights"].keys():
    settings = config["lights"][light_id]

    # Look for 'auto' in the value of a setting, replace with corresponding contents of auto
    # If not found, just take whatever's there
    kw = {}
    for k,v in settings.items():
        if v == "auto":
            kw[k] = auto[k]
        else:
            kw[k] = v

    # API call with kwargs. Update lightstates for scene
    bridge.scenes[scene_id].lightstates[light_id](**kw)

# Associate scene with button press on tap switch
bridge.rules[rule_id](actions=[
    {
    "address": "/groups/0/action",
    "method":  "PUT",
    "body":    {"scene": scene_id}
    }
], http_method="put")

# Tick a beat so we know things are always working.  See www.tickbeat.com
r = requests.post(config["tickbeat"]["url"], data={'doesnt':'matter'}, headers={"Authorization": "Bearer %s" % config["tickbeat"]["token"]})
