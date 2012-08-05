#!/usr/bin/python2.4

import psycopg2, itertools

# connect to database
# presumably we are using peer authentication and logged in as a user who has a pgsql account
try:
    conn = psycopg2.connect("dbname='otpprofiler'")
except:
    print "unable to connect to the database"

# Initialize the otpprofiler DB 'requests' table with query parameters
    
times = ["%02d:%02d:00" % (h, m) for h in range(5, 24, 2) for m in range(0, 60, 30)]
walks = [500, 1000, 2000, 3000, 5000, 10000, 2000000]
modes = ["WALK", "BICYCLE", "WALK,TRANSIT", "BICYCLE,TRANSIT"]
mins = ["QUICK"]
arriveBys = (True, False)

params = list(itertools.product(times, walks, modes, mins, arriveBys))

cur = conn.cursor()
cur.executemany("INSERT INTO requests (time, maxWalkDistance, modes, min, arriveBy) VALUES (%s, %s, %s, %s, %s)", params)
conn.commit()

# Initialize the otpprofiler DB with random endpoints

import csv
cur = conn.cursor()
endpoints = open("./endpoints.csv")
reader = csv.DictReader(endpoints)
sql = "INSERT INTO endpoints (random, location, name, notes) VALUES (true, %(point)s, 'rand'||%(n)s, %(name)s )"
for line in reader :
    line['point'] = "(%s,%s)" % (line['lon'], line['lat'])
    cur.execute(sql, line)
conn.commit()

