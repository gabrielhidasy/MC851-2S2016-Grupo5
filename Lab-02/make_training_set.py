#!/usr/bin/env python

import sys
import glob

fresh_ids = {}
hot_ids = {}

# fresh
for filename in glob.glob('9gag-fresh-*.dat'):
    lines = []
    time = filename[11:-4]
    with open (filename) as f:
        lines = f.readlines()
    for line in lines:
        url = line[20:-1]
        if url not in fresh_ids or time < fresh_ids[url]:
            fresh_ids[url] = time
 # hot
for filename in glob.glob('9gag-hot-*.dat'):
    lines = []
    time = filename[9:-4]
    with open (filename) as f:
        lines = f.readlines()
    for line in lines:
        url = line[20:-1]
        if url not in hot_ids or time < hot_ids[url]:
            hot_ids[url] = time      

# compare
for key, value in fresh_ids.items():
    if key in hot_ids:
        print ("{} {} {}".format(key, 1, int(hot_ids[key]) - int(fresh_ids[key])))
    else:
        print ("{} {} {}".format(key, 0, "INFINITE"))
