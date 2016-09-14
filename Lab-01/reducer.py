#!/usr/bin/env python

from operator import itemgetter
import sys
import json


rpf = {}
lavanderTownMap = {}
minLong = -75
minLat = 38
total ={}

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
    #x = int(pokemon_data["latitude"] - minLat) * 200)
    #y = int(abs(pokemon_data["longitude"] - minLong) * 200)
    x = round(pokemon_data["latitude"],2)
    y = round(pokemon_data["longitude"],2)

    try:
        lavanderTownMap[(pokemon_data["pokemon_name"],x,y)] += 1
    except KeyError:
        lavanderTownMap[(pokemon_data["pokemon_name"],x,y)] = 1

for (name,x,y) in sorted(lavanderTownMap):
    try:
        total[name] += 1
    except KeyError:
        total[name] = 1
    print ("{key} : {value}".format(key=(name,x,y), value=lavanderTownMap[(name,x,y)]))

print("Total = {value}".format(value=total))
