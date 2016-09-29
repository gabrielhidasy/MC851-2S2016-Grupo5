import xml.etree.ElementTree as ET
import time
import urllib.request

FRESH_URL = "http://www.15minutesoffame.be/9gag/rss/9GAG_-_Fresh.atom"
BASE_FRESH_FILE_NAME = "9gag-fresh-{}.dat"
HOT_URL = "http://www.15minutesoffame.be/9gag/rss/9GAG_-_Hot.atom"
BASE_HOT_FILE_NAME = "9gag-hot-{}.dat"

i = 0
while True:
    hot_response = urllib.request.urlopen(HOT_URL)
    hot_content = hot_response.read()
    hot_xml = ET.fromstring(hot_content)

    fresh_response = urllib.request.urlopen(FRESH_URL)
    fresh_content = fresh_response.read()
    fresh_xml = ET.fromstring(fresh_content)

    print("Iteration {}".format(i))
    i = i + 1
    hot_file_name = BASE_HOT_FILE_NAME.format(int(time.time()))
    fresh_file_name = BASE_FRESH_FILE_NAME.format(int(time.time()))
    
    try:
        with open(hot_file_name, "a+") as gag:
            for child in hot_xml:
                if "entry" in child.tag:
                    for entry in child:
                        if "link" in entry.tag:
                            gag.write("{}\n".format(entry.attrib["href"]))
                            
        with open(fresh_file_name, "a+") as gag:
            for child in fresh_xml:
                if "entry" in child.tag:
                    for entry in child:
                        if "link" in entry.tag:
                            gag.write("{}\n".format(entry.attrib["href"]))
    except KeyError:
        pass

    time.sleep(2*60)
    
