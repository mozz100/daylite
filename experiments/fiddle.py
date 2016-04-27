from qhue.qhue import Bridge
import json

with open("../hue_config.json", "r") as f:
    config = json.loads(f.read())
    hue = config["bridge"]

b = Bridge(hue["address"], hue["username"])

# create scene
b.scenes(name='daylite', lights=["6","9","11","12","13","14","15"], recycle=True, http_method='post')

# delete scene
#b.scenes('pr6MN1y-fKHjViO', http_method='delete')

# list scenes
for k,v in b.scenes().items():
	print k,v["name"]

# get scene
# print json.dumps(b.scenes('322f456e0-on-0'), indent=2)

# get lightstates
#print json.dumps(b.scenes['322f456e0-on-0'](), indent=2)

# mod lightstates. This works:
# curl -X PUT -H "Content-Type: application/json" -d '{"ct":200}' http://hue/api/<userid>/scenes/322f456e0-on-0/lights/6/state
# print json.dumps(b.scenes['322f456e0-on-0'].lightstates[6](on=True, bri=254, hue=25500), indent=2)
# red = 0, green = 25500
# for light_id in (6,9,11,12,13,14,15):
#     if light_id in (12,):
#         b.scenes['322f456e0-on-0'].lightstates[light_id](on=True, bri=254)
#     else:
#         b.scenes['322f456e0-on-0'].lightstates[light_id](on=True, bri=254, hue=0)

# list groups
#print json.dumps(b.groups(), indent=2)

# create group
#print json.dumps(b.groups(lights=['6','9'],name='mozzgrp',type="LightGroup",http_method='post'))

# delete group
#print json.dumps(b.groups(1, http_method='delete'))

# Apply a scene
# print json.dumps(b.groups[0].action(scene='322f456e0-on-0'))
# b.groups[0].action(scene='322f456e0-on-0')

# Update a rule
#print b.rules[config["rule_id"]](actions=[{"address":"/groups/0/action","method":"PUT","body": {"scene": config["scene_id"]}}], http_method="put")

# list rules
#print "\n---\n", json.dumps(b.rules(), indent=2)