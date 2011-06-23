#!/usr/bin/python

# A check_mk plugin to monitor the status of an HAProxy server.
# Hereward Cooper <coops@fawk.eu>

import os
import re
import sys

command="echo 'show stat' | nc -U /tmp/haproxy | egrep -v '(^#|^haproxystats)'"

titles="pxname,svname,qcur,qmax,scur,smax,slim,stot,bin,bout,dreq,dresp,ereq,econ,eresp,\
        wretr,wredis,status,weight,act,bck,chkfail,chkdown,lastchg,downtime,qlimit,\
        pid,iid,sid,throttle,lbtot,tracked,type,rate,rate_lim,rate_max,check_status,\
        check_code,check_duration,hrsp_1xx,hrsp_2xx,hrsp_3xx,hrsp_4xx,hrsp_5xx,\
        hrsp_other,hanafail,req_rate,req_rate_max,req_tot,cli_abrt,srv_abrt,misc"

title_array=titles.split(',')

checks = [
    ['bout', '512000', '1024000'],
    ['rate', '100', '500'],
    ['status', '', ''],
    ['downtime', '5', '25']
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
    for server in servers:

        if server['svname'] == "BACKEND" or server['svname'] == "FRONTEND":             # Skip FRONTEND and BACKEND lines
            continue

        # Define some variables
        result=""           # The complete set of results for each server's checks
        alert_warn=""       # Flag set if  check makes a server WARN
        alert_crit=""       #   "   "   "   "   "   "   "   "   CRIT
        alert_ok=""         #   "   "   "   "   "   "   "   "   OK

        for check,warn,crit in checks:
            output=""

            # Special check for the "status" field as it's not a numeric value
            if check == "status":
                if server['status'] == "UP":
                    output += "| status UP "
                if server['status'] == "DOWN":
                    output += "| status DOWN "
                    alert_crit = 1
    
            # Generic check for the other fields which are numeric
            else:
                if server[check] > warn and server[check] < crit:
                    output += "| " + check + " WARN " + server[check]
                    alert_warn = 1
                if server[check] > crit:
                    output += "| " + check + " CRIT " + server[check]
                    alert_crit = 1
                #if server[check] < warn:
                    #output += "| " + check + " OK " + server[check]

            # Append the outcome of check check to the results line for the server
            result += output

        # Determine if we need to flag the server as OK, WARN or CRIT
        if alert_warn==1:
            print "1 " + "HAProxy_" + server['svname'] + " - WARNING - " + result
        if alert_crit==1:
            print "2 " + "HAProxy_" + server['svname'] + " - CRITICAL - " + result
        if alert_crit != 1 and alert_warn != 1:
            print "0 " + "HAProxy_" + server['svname'] + " - OK " + result

servers = build_array()
run_checks()
