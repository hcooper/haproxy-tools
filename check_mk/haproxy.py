#!/usr/bin/python

import os
import re

command="echo 'show stat' | nc -U /tmp/haproxy | egrep -v '(^#|^haproxystats)'"
data = os.popen(command).read()

def build_array():
    services=[]
    for line in data.split('\n'):		# split out each line of raw input
        if re.match(r'^\s*$', line):
            continue
        holding=[]			# start a temp array
        for var in line.split(','):	# for each value append it to the temp array
            holding.append(var)
        services.append(holding)	# append the temp array to the services array
    return services

services = build_array()

for pxname,svname,qcur,qmax,scur,smax,slim,stot,bin,bout,dreq,dresp,ereq,econ,eresp,\
        wretr,wredis,status,weight,act,bck,chkfail,chkdown,lastchg,downtime,qlimit,\
        pid,iid,sid,throttle,lbtot,tracked,type,rate,rate_lim,rate_max,check_status,\
        check_code,check_duration,hrsp_1xx,hrsp_2xx,hrsp_3xx,hrsp_4xx,hrsp_5xx,\
        hrsp_other,hanafail,req_rate,req_rate_max,req_tot,cli_abrt,srv_abrt,misc in services:
        try:
            if svname != "FRONTEND":
                if svname != "BACKEND":
                    print svname + " (member of: " + pxname + ") status " + status
        except:
            continue
