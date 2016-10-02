#!/usr/bin/python2
import sys
import urllib
import urllib2
import re
import json
from pyspark import SparkContext, SparkConf
from pyspark.streaming import StreamingContext
import numpy as np
import cv2

def url_to_image(url):
    # Download the image, convert to numpy, read to OpenCV
    resp = urllib2.urlopen(url)
    image = np.asarray(bytearray(resp.read()), dtype="uint8")
    image = cv2.imdecode(umage, cv2.IMREAD_COLOR)
    return image

sc = SparkContext("local[4]", "NetworkWordCount")
ssc = StreamingContext(sc, 1)


title_regex = re.compile(r"<title>(.*)</title>", flags=re.MULTILINE)
image_regex = re.compile(r"<link rel=\"image_src\" href=\"(.*)\" />", flags=re.MULTILINE)
points_regex = re.compile(r"data-entry-votes=\"([0-9]*)\"", flags=re.MULTILINE)
comment_url = "http://comment-cdn.9gag.com/v1/cacheable/comment-list.json"
comment_data = {
    'appId' : 'a_dd8f2b7d304a10edaf6f29517ea0ca4100a43d1b',
    'url' : 'http://9gag.com/gag/{}',
    'count' : 100,
    'level' : 1,
    'order' : 'score'
    }

def download_post(URL):
    try:
        post_id = URL.split("/")[4][:7]
        print("Called with post_id = {}", post_id)
        request = urllib2.urlopen(URL)
        raw_post = request.read()
        post_title = title_regex.search(raw_post).group(1)
        image_url = image_regex.search(raw_post).group(1)
        points = int(points_regex.search(raw_post).group(1))
        image = url_to_image(image_url)
        histogram = cv2.calcHist([image], [0], None, [256], [0, 256])
        image_descriptor = histogram
        this_comment = comment_data.copy()
        this_comment["url"] = this_comment["url"].format(post_id)
        this_comment_url = "{}?{}".format(comment_url, urllib.urlencode(this_comment))
        request = urllib2.urlopen(this_comment_url)
        raw_comments = json.loads(request.read())["payload"]
        num_comments = int(raw_comments["total"])
        raw_comments = raw_comments["comments"]
        comments = [(x["user"]["displayName"], x["text"]) for x in raw_comments]
        image_descriptor = 0
        return (post_id, post_title, points, image_descriptor, comments, 2)
    except Exception as e:
        with open("exlog", "a+") as f:
            f.write(str(e)+"\n")
        return ()


URLs = ssc.socketTextStream("localhost", 9999)
print(URLs.count())
if URLs.count():
        posts = URLs.map(download_post)
        posts.saveAsTextFiles("posts-","dat")

ssc.start()
ssc.awaitTermination()


#URLs = ["http://9gag.com/gag/aopoK4x"]
#print(map(download_post, URLs))
