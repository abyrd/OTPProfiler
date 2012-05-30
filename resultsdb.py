#!/usr/bin/python

import sqlite3, os, random

class ResultsDatabase :

    def __init__(self):
        filename = 'results.sqlite'
        init = False
        if not os.path.exists(filename):
            init = True
        self.conn = sqlite3.connect(filename)
        if init :
            self.setup()
        
    def setup(self):
        c = self.conn.cursor()
        c.execute( "CREATE TABLE graphs (id INTEGER PRIMARY KEY, path TEXT, centerlat FLOAT, centerlon FLOAT, stdlat FLOAT, stdlon FLOAT)" )
        c.execute( "CREATE TABLE runs (id INTEGER PRIMARY KEY, timestamp DATETIME, githash TEXT UNIQUE ON CONFLICT IGNORE)" )
        c.execute( "CREATE TABLE requests ()" )
        c.execute( "CREATE TABLE results (id INTEGER PRIMARY KEY, nitineraries INTEGER, time INTEGER, membytes INTEGER)" )
        c.execute( "CREATE TABLE itineraries (id INTEGER PRIMARY KEY, nitineraries INTEGER, time INTEGER, membytes INTEGER)" )
        c.execute( "CREATE TABLE endpoints (id INTEGER PRIMARY KEY, graph INTEGER, name TEXT, lon FLOAT, lat FLOAT)" )
        c.execute( "CREATE TABLE random_endpoints (id INTEGER PRIMARY KEY, olon FLOAT, olat FLOAT, dlon FLOAT, dlat FLOAT)" )
        self.conn.commit()
        c.close()
    
    def generate_endpoints():
        #random endpoints
        N = 500
        c = self.conn.cursor()
        for i in range(N) :
            olat = random.gauss(CENTER[0], STDEV[0])
            olon = random.gauss(CENTER[1], STDEV[1])
            c.execute("INSERT INTO gaussian_endpoints VALUES (?,?,?,?)", (i, lon[0])
                # print "%f,%f" % (lat, lon)

    def populate_endpoints():
        #defined endpoints
        for line in open('endpoints'):
            fields = line.strip().split(',')
            if len(fields) != 3:
                print 'line does not have 3 fields'
            else:
                name, lat, lon = fields
                endpoints.


        endpoints = {}
                endpoints[name] = (float(lat),float(lon))

def main():
    db = ResultsDatabase()

if __name__=='__main__':
    main()
