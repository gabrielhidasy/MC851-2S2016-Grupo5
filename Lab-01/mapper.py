#!/usr/bin/env python

# Mapper application for pokemon filter
# This mapper filters out pokemons that are not being searched

import sys
import json

pokemon_target = sys.argv[1].split(",")
# input comes from STDIN (standard input)
for line in sys.stdin:
    pokedata_full = json.loads(line)
    pokedata = {}
    # TODO: Search for pokemon ids (will require table)
    if pokedata_full["pokemon_name"] not in pokemon_target:
        continue
    for key in ["pokemon_id", "latitude", "longitude", "expires"]:
        pokedata[key] = pokedata_full[key]
    record_id = (10000*pokedata["pokemon_id"] +
                 1000*pokedata["latitude"] +
                 pokedata["longitude"])
    print("{}\t{}".format(record_id, json.dumps(pokedata)))
