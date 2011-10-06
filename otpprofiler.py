#!/usr/bin/python

import sqlite3
db = sqlite3.connect("profile_results.sqlite")

URL = "http://localhost/otp?fromPlace=%f,%f&toPlace=%f,%f&min=%s&maxWalkDistance=%d&mode=%s&submit&time=%s&arriveBy=%s"

for time in ["%02d:%02d" % (h, m) for h in range(24) for m in range(0, 60, 30)] :
    for arrive_by in ("TRUE", "FALSE") :
        for mode in ("WALK", "BICYCLE", "WALK,TRANSIT", "BICYCLE,TRANSIT") :
            print URL % (0,0,0,0,"QUICK",1000,mode,time,arrive_by)

