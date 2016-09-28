#!/usr/bin/python2
import sys
import urllib
import urllib2
import re
import json

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

for URL in sys.stdin:
    post_id = URL.split("/")[4][:7]
    print(post_id)
    request = urllib2.urlopen(URL)
    raw_post = request.read()
    post_title = title_regex.search(raw_post).group(1)
    image_url = image_regex.search(raw_post).group(1)
    points = int(points_regex.search(raw_post).group(1))
    print(post_title)
    print(image_url)
    print(points)
    this_comment = comment_data.copy()
    this_comment["url"] = this_comment["url"].format(post_id)
    this_comment_url = "{}?{}".format(comment_url, urllib.urlencode(this_comment))
    print(this_comment_url)
    request = urllib2.urlopen(this_comment_url)
    raw_comments = json.loads(request.read())["payload"]
    num_comments = int(raw_comments["total"])
    raw_comments = raw_comments["comments"]
    comments = [(x["user"]["displayName"], x["text"]) for x in raw_comments]
