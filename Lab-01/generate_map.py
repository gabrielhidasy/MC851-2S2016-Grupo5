#!/usr/bin/python
import ast
import matplotlib.pyplot
import mpl_toolkits.basemap
import numpy
import sys

# Personally I would use:
# llcrnrlon=-75.0, llcrnrlat=40.5, urcrnrlon=-72.7, urcrnrlat=41.3,

map = mpl_toolkits.basemap.Basemap(projection='mill',
                                   resolution='f',
                                   llcrnrlon=-75.0,
                                   llcrnrlat=40.0,
                                   urcrnrlon=-70.0,
                                   urcrnrlat=42.0,
                                   area_thresh=10000.0)

#map.drawcoastlines()
#map.drawcountries()
map.shadedrelief()
#map.fillcontinents(color='green')
map.drawmeridians(numpy.arange(0, 360, 0.3))
map.drawparallels(numpy.arange(-90, 90, 0.3))
map.drawmapboundary()

color_list = ["green", "red", "yellow", "blue", "orange", "purple", "black", "white"]
color_n = 0
color_table = {}
for line in sys.stdin:
    try:
        position, size = line.split(":")
        size = int(size)
        position = ast.literal_eval(position)
        color = ""
        do_label = False
        if position[0] in color_table:
            color = color_table[position[0]]
        else:
            color_table[position[0]] = color_list[color_n]
            color = color_list[color_n]
            color_n += 1
            do_label = True
            if color_n == len(color_list):
                color_n = 0
        if do_label:
            map.plot(position[2],
                     position[1],
                     "D",
                     color=color,
                     markersize=10,
                     alpha=0.5,
                     latlon=True,
                     label=position[0])
            print(color)
        else:
            map.plot(position[2],
                     position[1],
                     "D",
                     color=color,
                     markersize=10,
                     alpha=0.5,
                     latlon=True)
    except ValueError:
        pass
matplotlib.pyplot.legend()
matplotlib.pyplot.show()
#plt.savefig('map.png')


