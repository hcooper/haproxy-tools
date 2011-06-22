#!/usr/bin/python

# A check_mk plugin to monitor the status of an HAProxy server.
# Hereward Cooper <coops@fawk.eu>

import os
import re

command="echo 'show stat' | nc -U /tmp/haproxy | egrep -v '(^#|^haproxystats)'"

# Convert the raw stats into nested arrays. Much nicer to use.
def build_array():
    data = os.popen(command).read()     # Retrieve the raw data
    services=[]
    for line in data.split('\n'):		# split out each line of raw input
        if re.match(r'^\s*$', line):    # skip empty lines
            continue
        services.append( line.split(',') )
    return services

services = build_array()

checks = [
        ['rate', '10', '20'],
        ['chkfail', '10', '20']
]

for pxname,svname,qcur,qmax,scur,smax,slim,stot,bin,bout,dreq,dresp,ereq,econ,eresp,\
        wretr,wredis,status,weight,act,bck,chkfail,chkdown,lastchg,downtime,qlimit,\
        pid,iid,sid,throttle,lbtot,tracked,type,rate,rate_lim,rate_max,check_status,\
        check_code,check_duration,hrsp_1xx,hrsp_2xx,hrsp_3xx,hrsp_4xx,hrsp_5xx,\
        hrsp_other,hanafail,req_rate,req_rate_max,req_tot,cli_abrt,srv_abrt,misc in services:
        try:
            if svname != "FRONTEND" and svname != "BACKEND":
                print svname + " (member of: " + pxname + ") status " + status + " rate: " + rate + " failed checks: " + chkfail
        except:
            continue

        #for check,warn,crit in checks:
        #    print check
            
