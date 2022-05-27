#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tweepy, os, requests, sys
from PIL import Image
from secrets import *
white_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'white.png')


def twitter_api():
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    api = tweepy.API(auth)
    return api

def tweet_image(url_list, message):
    api = twitter_api()
    filenames = []
    for index, url in enumerate(url_list):
        filenames.append('temp%s.jpg' % index)
    media_ids = []
    url_tuple = zip(filenames, url_list)
    for i in range(len(url_tuple)):
        file, url = url_tuple[i]
        request = requests.get(url, stream=True)
        if request.status_code == 200:
            with open(file, 'wb') as image:
                for chunk in request:
                    image.write(chunk)
            image.close()
            foreground = Image.open(file)
            background = Image.open(white_file)
            background.paste(foreground, (0, 0), foreground.convert('RGBA'))
            background.save(file)
            res = api.media_upload(file)
            media_ids.append(res.media_id)
        else:
            print("Unable to download image")
            break
    api.update_status(status=message, media_ids=media_ids)
    for temp in filenames:
        os.remove(temp)

if '__main__' in __name__:
    pdbid = sys.argv[0]
    url = "http://www.ebi.ac.uk/pdbe/static/entry/%s_assembly_1_chemically_distinct_molecules_front_image-800x800.png" % pdbid
    message = "Here is the structure of pdb ID %s. Find it at PDBe.org/%s" % (pdbid, pdbid)
    tweet_image(url, message)
