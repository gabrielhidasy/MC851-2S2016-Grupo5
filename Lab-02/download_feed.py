import xml.etree.ElementTree as ET
import time
import urllib.request

URL = "http://www.15minutesoffame.be/9gag/rss/9GAG_-_Fresh.atom"
BASE_FILE_NAME = "9gag-{}.dat"

i = 0
while True:
    response = urllib.request.urlopen(URL)
    content = response.read()
    e = ET.fromstring(content)

    print("Iteration {}".format(i))
    i = i + 1
    file_name = BASE_FILE_NAME.format(int(time.time()))
    
    try:
        with open(file_name, "a+") as gag:
            for child in e:
                if "entry" in child.tag:
                    for entry in child:
                        if "link" in entry.tag:
                            gag.write("{}\n".format(entry.attrib["href"]))
    except KeyError:
        pass

    time.sleep(2*60)
    
