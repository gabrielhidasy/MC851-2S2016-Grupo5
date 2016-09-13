#!/usr/bin/env python

from operator import itemgetter
import sys

from mpl_toolkits.basemap import Basemap
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

maxsize = -5000
lat_dic = {}
#for i in range(-128,128):
#    lat_dic[i] = {}
    
# input comes from STDIN
for line in sys.stdin:
    # parse the input we got from mapper.py
    print(line)
    lats, lons = line.split('\t', 1)
    # convert count (currently a string) to int
    try:
        lat = float(lats)
        lon = float(lons)
    except ValueError:
        # count was not a number, so silently
        # ignore/discard this line
        print("PAU")
        continue
    print(lat,lon)
    # this IF-switch only works because Hadoop sorts map output
    # by key (here: word) before it is passed to the reducer
    #coords[lat+127][lon+127] = coords[lat+127][lon+127] + 1
    try:   
        lat_dic[(lat,lon)] = lat_dic[(lat,lon)] + 1
        if(lat_dic[(lat,lon)] > maxsize):
            maxsize = lat_dic[(lat,lon)]
    except:
        lat_dic[(lat,lon)] = 1

print("Reduce step finished, plotting data")

def find_max(d):
    v=list(d.values())
    k=list(d.keys())
    return k[v.index(max(v))]

map = Basemap(projection='robin', lat_0=50, lon_0=0,
              resolution='l', area_thresh=1000.0)

map.drawcoastlines()
map.drawcountries()
map.fillcontinents(color='green')
map.drawmeridians(np.arange(0, 360, 30))
map.drawparallels(np.arange(-90, 90, 30))
map.drawmapboundary()

#Choose only k best points to plot
points = []
k = 1000
for i in range(1,k):
    tmp = find_max(lat_dic)
    points.append((tmp,lat_dic[tmp]))
    lat_dic[tmp] = 0
for p in points:
    x,y = map(p[0][1],p[0][0])
    size = max((p[1]/maxsize)*50,3)
    map.plot(x,y,'bo',markersize=size)

#for key in lat_dic:
#    x,y = map(key[1],key[0])
#    size = max(((lat_dic[key]/maxsize)*50),1)
#    map.plot(x,y,'bo',markersize=size)

plt.show()
#plt.savefig('map.png')
print(points)
#print(maxla,minla,maxlo,minlo)
#print(lat_dic)
