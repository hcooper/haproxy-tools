data="""web,FRONTEND,,,0,0,4096,0,0,0,0,0,0,,,,,OPEN,,,,,,,,,1,2,0,,,,0,0,0,0,,,,0,0,0,0,0,0,,0,0,0,,,
mysql,FRONTEND,,,0,0,4096,0,0,0,0,0,0,,,,,OPEN,,,,,,,,,1,3,0,,,,0,0,0,0,,,,,,,,,,,0,0,0,,,
web-https,FRONTEND,,,0,0,4096,0,0,0,0,0,0,,,,,OPEN,,,,,,,,,1,4,0,,,,0,0,0,0,,,,,,,,,,,0,0,0,,,
web,web2-NEW,0,0,0,0,,0,0,0,,0,,0,0,0,0,UP,1,0,1,0,0,19,0,,1,5,1,,0,,2,0,,0,L4OK,,0,0,0,0,0,0,0,0,,,,0,0,
web,web1-OLD,0,0,0,0,,0,0,0,,0,,0,0,0,0,UP,1,1,0,0,0,19,0,,1,5,2,,0,,2,0,,0,L4OK,,0,0,0,0,0,0,0,0,,,,0,0,
web,BACKEND,0,0,0,0,0,0,0,0,0,0,,0,0,0,0,UP,1,1,1,,0,19,0,,1,5,0,,0,,1,0,,0,,,,0,0,0,0,0,0,,,,,0,0,
web-https,web2-NEW,0,0,0,0,,0,0,0,,0,,0,0,0,0,UP,1,0,1,0,0,19,0,,1,6,1,,0,,2,0,,0,L4OK,,0,,,,,,,0,,,,0,0,
web-https,web1-OLD,0,0,0,0,,0,0,0,,0,,0,0,0,0,UP,1,1,0,0,0,19,0,,1,6,2,,0,,2,0,,0,L4OK,,0,,,,,,,0,,,,0,0,
web-https,BACKEND,0,0,0,0,0,0,0,0,0,0,,0,0,0,0,UP,1,1,1,,0,19,0,,1,6,0,,0,,1,0,,0,,,,,,,,,,,,,,0,0,
mysql,db2-NEW,0,0,0,0,,0,0,0,,0,,0,0,0,0,UP,1,0,1,0,0,19,0,,1,7,1,,0,,2,0,,0,L7OK,0,13,,,,,,,0,,,,0,0,
mysql,db1-OLD,0,0,0,0,,0,0,0,,0,,0,0,0,0,UP,1,1,0,0,0,19,0,,1,7,2,,0,,2,0,,0,L7OK,0,4,,,,,,,0,,,,0,0,
mysql,BACKEND,0,0,0,0,0,0,0,0,0,0,,0,0,0,0,UP,1,1,1,,0,19,0,,1,7,0,,0,,1,0,,0,,,,,,,,,,,,,,0,0,"""

def build_array():
	services=[]
	for line in data.split('\n'):		# split out each line of raw input
		holding=[]			# start a temp array
		for var in line.split(','):	# for each value append it to the temp array
			holding.append(var)
		services.append(holding)	# append the temp array to the services array
	return services
services = build_array()

for server in services:
	if server[1] != "FRONTEND":
		if server[1] != "BACKEND":
			print server[1] + " (member of: " + server[0] + ") status " + server[17]
