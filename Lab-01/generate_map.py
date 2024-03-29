#!/usr/bin/python
import matplotlib.pyplot as plt
from datetime import datetime
from mpl_toolkits.basemap import Basemap
import numpy as np
import sys
from ast import literal_eval

# Personally I would use:
# llcrnrlon=-75.0, llcrnrlat=40.5, urcrnrlon=-72.7, urcrnrlat=41.3,

map = Basemap(projection='mill',
               resolution='h',
              llcrnrlon=-75.0,
              llcrnrlat=40.0,
              urcrnrlon=-70.0,
              urcrnrlat=42.0,
              area_thresh=10000.0)

#map.drawcoastlines()
#map.drawcountries()
map.shadedrelief()
#map.fillcontinents(color='green')
map.drawmeridians(np.arange(0, 360, 0.3))
map.drawparallels(np.arange(-90, 90, 0.3))
map.drawmapboundary()

for line in sys.stdin:
    try:
        position, size = line.split(":")
        size = int(size)
        position = literal_eval(position)
        print(position)
        map.plot(position[2],
                 position[1],
                 "rD",
                 markersize=10,
                 alpha=0.1,
                 latlon=True)
    except ValueError:
        pass

plt.show()
#plt.savefig('map.png')

    
