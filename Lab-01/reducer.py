#!/usr/bin/env python

from operator import itemgetter
import sys
import json

#import matplotlib.pyplot as plt
from datetime import datetime


rpf = {}
lavanderTownMap = {}
minLong = int(-75)
minLat = int(38)

#pokegrid = [[0]*(5000/0.2) for x in range((5000/0.2))]
# input comes from STDIN
for line in sys.stdin:
    try:
        hadoop_id, pokemon_data = line.split("\t")
    except:
        print("Offending line: {}".format(line))
        continue

    try:
        pokemon_data = json.loads(pokemon_data)
    except:
        print("Offending line 2: {}".format(line))
        print(pokemon_data)
        continue

    if hadoop_id in rpf:
        dup = False
        for p in rpf[hadoop_id]:
            if abs(p-pokemon_data["expires"]) < 200:
                dup = True
                break
        if dup:
            continue
    try:
        rpf[hadoop_id].append(pokemon_data["expires"])
    except KeyError:
        rpf[hadoop_id] = [pokemon_data["expires"]]

    #print(pokemon_data)
    y = int((pokemon_data["latitude"] - minLat) * 200)
    x = int(abs(pokemon_data["longitude"] - minLong) * 200)

    try:
        lavanderTownMap[(x,y)] += 1
    except KeyError:
        lavanderTownMap[(x,y)] = 1

print(lavanderTownMap)
