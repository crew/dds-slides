#!/usr/bin/python
__author__ = 'Jeff Dlouhy <jdlouhy@ccs.neu.edu>'

import os
import sys
import json
import urllib

def start_convert(filename):
    print os.path.abspath(filename)
    jsfile = open(os.path.abspath(filename), 'r')
    jsblob = json.load(jsfile);
    children = jsblob['children']
    for child in children:
        if "url" in child and "filename" in child:
            url = child['url']
            imgfilename = child['filename']
            download_image(url, imgfilename)
            #picfile = open(os.path.abspath(filename), 'r')
            #del child['url']

    jsfile.close()
    jsfile = open(os.path.abspath(filename), 'w')
    json.dump(jsblob, jsfile)
    jsfile.close()


# def get_image_textures(self, jsonblob):
def download_image(url, imgfile):
    urllib.urlretrieve(url, imgfile)

if __name__ == '__main__':
    args = sys.argv
    if len(args) > 1:
        filename = args[1]
        if os.path.exists(filename):
            start_convert(filename)
