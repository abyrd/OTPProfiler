#!/usr/bin/python

import random, urllib, urllib2, time, json
from math import exp
from violin import violin_plot
import numpy as np
import matplotlib.pyplot as plot

N_TRIPS = 200
CENTER = (38.8972, -77.017)
STDEV = (0.1, 0.1)

def quantile(data, q, presorted = False) :
    """
    Linear interpolation of the empirical distribution function.
    """
    if not presorted :
        data = sorted(data)
    n = len(data)
    real_index = n * q
    if real_index <= 0 :
        real_index = 0
    if real_index >= n - 1 :
        real_index = n - 1
    int_index = int(real_index)
    frac_index = real_index - int_index
    low = data[int_index]
    if frac_index == 0 :
        return low
    high = data[int_index + 1]
    interp = low + frac_index * (high - low)
    return interp

def mean(data) :
    return sum(data) / len(data)

def expdist_cumulative(param, x) :
    return 1 - exp(-param * x)

def expdist_density(param, x) :
    return param * exp(-param * x)

random.seed(12345)
os = []
ds = []
for i in range(N_TRIPS) :
    for l in [os, ds] :
        lat = random.gauss(CENTER[0], STDEV[0])
        lon = random.gauss(CENTER[1], STDEV[1])
        l.append((lat, lon))
        # print "%f,%f" % (lat, lon)

URL = "http://localhost:8080/opentripplanner-api-webapp/ws/plan?"
totalItin = 0
totalTime = 0
totalResponses = 0
results = []
times = []
for i in range(N_TRIPS) :
    o = os[i]
    d = ds[i]
    # print o, d
    arriveBy = False
    # Sets up the URL parameters
    params =  {'time' : '8:00 AM',
               'fromPlace' : '%s,%s' % o,
               'toPlace' :   '%s,%s' % d,
               'maxWalkDistance' : 2000,
               'mode' : 'WALK,TRANSIT', 
               'date' : '2012-05-15',
               'numItineraries' : 3, 
               'arriveBy' : 'true' if arriveBy else 'false' }
    url = URL + urllib.urlencode(params)
    req = urllib2.Request(url)
    req.add_header('Accept', 'application/json')
    # print url
    try :
        start = time.time()
        response = urllib2.urlopen(req) 
        end = time.time()
        t = end - start
    except urllib2.HTTPError as e :
        print e
        continue
    try :
        content = response.read()
        objs = json.loads(content)
        itineraries = objs['plan']['itineraries']
    except :
        print 'no itineraries'
        continue
    print '%0.3f sec %s %d/%d' % (t, response.code, len(itineraries), params['numItineraries'])
    # results.append(describe(itin) for itin in itineraries)
    totalItin += len(itineraries)
    totalResponses += 1
    totalTime += t
    times.append(t)

print 'total itineraries %d, total time %0.3f, avg time per itinerary %0.3f' % (totalItin, totalTime, totalTime / totalItin)
print 'itineraries per second:', float(totalResponses) / totalTime
xbar = mean(times)
param = 1/xbar
print 'mean', xbar
print 'maximum likelihood parameter for exponential distribution:', param
times.sort()
q = 0
# plot empirical and parametric distribution
for i in range(0, 20) :
    empirical = quantile(times, q, presorted = True)
    parametric = expdist_cumulative(param, empirical)
    print empirical, q, parametric, expdist_density(param, empirical) 
    q += 0.05

pos = range(4)
data = [times for i in pos]
fig = plot.figure()
ax = fig.add_subplot(111)
violin_plot(ax,data,pos,bp=True)
plot.show()





