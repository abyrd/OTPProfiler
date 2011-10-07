#!/usr/bin/python

import sqlite3
db = sqlite3.connect("profile_results.sqlite")

URL = "http://localhost/otp?fromPlace=%f,%f&toPlace=%f,%f&min=%s&maxWalkDistance=%d&mode=%s&submit&time=%s&arriveBy=%s"

times = ["%02d:%02d" % (h, m) for h in range(24) for m in range(0, 60, 30)]
modes = ["WALK", "BICYCLE", "WALK,TRANSIT", "BICYCLE,TRANSIT"]
walks = [500, 1000, 2000, 3000, 5000, 10000, 20000]

#runid = time;
#db.execute("insert % into runs");

for time in times:
    for arrive_by in ("TRUE", "FALSE") :
        for mode in modes :
            for walk in walks :
                print URL % (0,0,0,0,"QUICK",walk,mode,time,arrive_by)

