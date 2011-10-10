#!/usr/bin/python

import sqlite3, urllib2, time, itertools
# ubuntu package python-beautifulsoup
from BeautifulSoup import BeautifulStoneSoup
import random

import json

db = sqlite3.connect("profile_results.sqlite")

times = ["%02d:%02d" % (h, m) for h in range(24) for m in range(0, 60, 30)]
modes = ["WALK", "BICYCLE", "WALK,TRANSIT", "BICYCLE,TRANSIT"]
walks = [500, 1000, 2000, 3000, 5000, 10000, 20000]

#runid = time;
#db.execute("insert % into runs");

endpoints = {}
for line in open('endpoints'):
    fields = line.strip().split(',')
    if len(fields) != 3:
        print 'line does not have 3 fields'
    else:
        name, lat, lon = fields
        endpoints[name] = (float(lat),float(lon))
print endpoints

URL = "http://localhost:8080/opentripplanner-api-webapp/ws/plan?submit&fromPlace=%f,%f&toPlace=%f,%f&min=%s&maxWalkDistance=%d&mode=%s&submit&time=%s&date=09/14/2011&arr=%s"

total = 0
worst = 0
worst_url = None
durations = []
x = list(itertools.product(modes, times, walks, ('Depart','Arrive'), endpoints.items(), endpoints.items()))
random.shuffle(x)
for r in x :
#for r in itertools.product(modes, times, walks, ('Depart','Arrive'), endpoints.items(), endpoints.items()) :
    print r
    (mode, t, walk, arrive_by, orig, dest) = r
    o_name, o_coord = orig
    d_name, d_coord = dest
    if o_name == d_name :
        continue
    print '%s to %s' % (o_name, d_name)
    url = URL % (o_coord[0],o_coord[1],d_coord[0],d_coord[1],"QUICK",walk,mode,t,arrive_by)
    req = urllib2.Request(url)
    req.add_header('Accept', 'APPLICATION/XML')
    start = time.time()
    response = urllib2.urlopen(req).read()
    end = time.time()
    #print response
    #response = json.loads(response)
    #print json.dumps(response, sort_keys=False, indent=4)
    soup = BeautifulStoneSoup(response)
    #print soup.prettify()
    #if 'error' in response :
    #    print 'error'
    #    continue
    #nItin = len(response['plan']['itineraries']['itinerary'])
    if (soup.response.error != None) :
        print 'error'
        continue
    nItin = len(soup.response.plan.itineraries)
    print nItin, 'itineraries'
    duration = end - start
    total += duration
    print duration, 'sec'
    print url
    durations.append(duration)
    if duration > worst:
        worst = duration
        worst_url = url

durations.sort()
#print durations
print "median", durations[(len(durations)-1)/2]
print "average", (total / len(urls))
print "worst", worst
#print "worst url", worst_url


