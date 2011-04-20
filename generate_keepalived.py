#!/usr/bin/python

# This script scans the haproxy configuration and generates the keepalived config to match
# Hereward Cooper - Apr 2011

import subprocess
from subprocess import Popen, PIPE, STDOUT

getips = subprocess.Popen(["/usr/local/bin/haproxy_check_ips.sh"], shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
VIPS = getips.stdout.read()

VIPINT = "eth1"
PRIORITY = "101"

OUTPUT = """
## /etc/keepalived/keepalived.conf
## THIS CONFIGURATION IS AUTOMATICALLY GENERATED.
## MANUAL CHANGES WILL BE OVERWRITTEN.

vrrp_script chk_haproxy {               # Requires keepalived-1.1.13
        script "killall -0 haproxy"     # cheaper than pidof
        interval 2                      # check every 2 seconds
        weight 2                        # add 2 points of prio if OK
}

vrrp_instance VI_1 {
        interface """ + VIPINT + """
        state MASTER
        virtual_router_id 51
        priority """ + PRIORITY + """			# 101=master, 100=standby
        virtual_ipaddress {
		""" + VIPS + """
        }
        track_script {
            chk_haproxy
        }
}
"""
print OUTPUT

