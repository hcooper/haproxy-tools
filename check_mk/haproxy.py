#!/usr/bin/python

# A check_mk plugin to monitor the status of an HAProxy server.
# Hereward Cooper <coops@fawk.eu>

import os
import re

command="echo 'show stat' | nc -U /tmp/haproxy | egrep -v '(^#|^haproxystats)'"

titles="pxname,svname,qcur,qmax,scur,smax,slim,stot,bin,bout,dreq,dresp,ereq,econ,eresp,\
        wretr,wredis,status,weight,act,bck,chkfail,chkdown,lastchg,downtime,qlimit,\
        pid,iid,sid,throttle,lbtot,tracked,type,rate,rate_lim,rate_max,check_status,\
        check_code,check_duration,hrsp_1xx,hrsp_2xx,hrsp_3xx,hrsp_4xx,hrsp_5xx,\
        hrsp_other,hanafail,req_rate,req_rate_max,req_tot,cli_abrt,srv_abrt,misc"

title_array=titles.split(',')

checks = [
    ['bout', '512000', '1024000'],
    ['status', '', '']
]


# Convert the raw stats into nested arrays. Much nicer to use.
def build_array():
    data = os.popen(command).read()     # Retrieve the raw data
    servers=[]
    for line in data.split('\n'):		# split out each line of raw input
        if re.match(r'^\s*$', line):    # skip empty lines
            continue
        i=0
        dict={}
        for var in line.split(','):         # for each value put it in a dictonary matching the human readable name in "title_array"
                dict[title_array[i]]=var
                i=i+1
        servers.append(dict)

    return servers


def run_checks():
    for check,warn,crit in checks:
        for server in servers:
    
            # Special check for the "status" field as it's not a numeric value
            if check == "status":
                if server['status'] == "UP":
                    print "OK"
                if server['status'] == "DOWN":
                    print "DOWN"
    
            # Generic check for the other fields which are numeric
            else:
                if server['svname'] == "BACKEND" or server['svname'] == "FRONTEND":             # Skip FRONTEND and BACKEND lines
                 continue
                if server[check] > warn and server[check] < crit:
                 print "1 HAProxy_" + server['svname'] + "_" + check + " - " + "WARNING - " + server['svname'] + " " + check + ": " + server[check]
                if server[check] > crit:
                 print "2 HAProxy_" + server['svname'] + "_" + check + " - " + "CRITICAL - " + server['svname'] + " " + check + ": " + server[check]
                if server[check] < warn:
                 print "0 HAProxy_" + server['svname'] + "_" + check + " - " + "OK - " + server['svname'] + " " + check + ": " + server[check]

servers = build_array()
run_checks()
