#!/bin/bash

# Script to check that the IPs HAProxy is listening on are also listed in the keepalived config

HACONFIGFILE="/etc/haproxy/haproxy.cfg"
KACONFIGFILE="/etc/keepalived/keepalived.conf"
TEMPFILE=`mktemp`

# Find all the 'listen' and 'frontend' lines from the haproxy configuration, and extract the IP address
egrep '(listen|frontend)' $HACONFIGFILE | grep -o '[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}' | grep -v 127.0.0.1 > $TEMPFILE

sort $TEMPFILE | uniq

## Strip out repeat entries in the list of IPs then check for them in the keepalived config
#echo "Comparing HAProxy and Keepalived configs"
#echo "========================================"
#for i in `sort $TEMPFILE | uniq`; do
#	grep -q $i $KACONFIGFILE &&
#	echo "$i -- OK" ||
#	echo "$i -- NO MATCH";
#done

# Tidy up
rm -f $TEMPFILE
