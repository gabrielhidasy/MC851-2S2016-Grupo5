#!/usr/bin/env python

import sys
import json

# input comes from STDIN (standard input)
for line in sys.stdin:
    # Split the line between epoch and pokemon data
    pokedata_full = json.loads(line)
    pokedata = {}
    for key in ["pokemon_id", "latitude", "longitude"]:
        pokedata[key] = pokedata_full[key]
    print(pokedata)
