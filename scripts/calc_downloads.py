#!/usr/bin/python
# -*- coding: utf-8 -*-

import re

LOG = "oi_podcast.log"
EPISODELIST = range(1, 13)

def get_amount_list():
    log_list = file(LOG).readlines()
    amount_list = []

    for line in log_list:
        m = re.search('(?<=oi_podcast_E)\w+.(mp3|ogg)', line)
        try:
            amount_list.append(m.group())
        except:
            # Example:
            #    78.174.192.97 - - [03/Apr/2010:19:55:49 +0300] "GET /media/podcasts/oi_podcast_E0/.ogg HTTP/1.1" 404 196
            #    78.174.241.181 - - [10/Apr/2010:19:13:30 +0300] "GET /media/podcasts/oi_podcast_E0*.ogg HTTP/1.1" 404 198
            pass

    return amount_list

def print_output():
    amount_list = get_amount_list()

    for episode in EPISODELIST:
        if episode < 10:
            episode = "0%s" % episode
        amount_ogg = amount_list.count('%s.ogg' % episode)
        amount_mp3 = amount_list.count('%s.mp3' % episode)

        print("podcast %s (toplam: %s)" % (episode, (amount_ogg + amount_mp3)))
        print("    ogg: %s" % amount_ogg)
        print("    mp3: %s\n" % amount_mp3)

if __name__ == "__main__":
    print_output()
