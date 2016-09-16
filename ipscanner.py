#!/usr/bin/python
import sh
import sys
from netaddr import *

def help():
    print """
        This script will scan any given IP range via a single address range
        or a file with multiple ranges

        Usage:
        ipscan.py [OPTIONS]
        -h or --help
        displays this usage notice

        -i or --ip <"IPRANGE/NETMASK">
        use this option for a single IP range (-i 192.168.1.1/24)

        -f or --file <"FILENAME">
        use this option to load a file with multiple IP ranges

        -m
        auto loads the F5_Networks file and scans for dead IPs
          """
    sys.exit()
def single_ip(Display_alive):
    print "Scanning IP Range"
    IP_list=[]
    address=sys.argv[2]
    for ip in IPNetwork(address):
        IP_list.append(ip)
    for num in xrange(0,len(IP_list)):
        try:
        #bash equivalent: ping -c 1 > /dev/null
            sh.ping(IP_list[num], "-c 1 -i 0.2", _out="/dev/null")
            if Display_alive.lower()== "y":
                print "ping to", IP_list[num], "OK"
        except sh.ErrorReturnCode_1:
            print "no response from", IP_list[num]
    sys.exit()
def file_scan(Display_alive):
    print "Opening File and beging scan"
    with open(sys.argv[2], 'r') as f:
        address=f.readlines()
    address=[x.strip('\n') for x in address]
    IP_list=[]
    for i in xrange(0,len(address)):
        for ip in IPNetwork(address[i]):
            IP_list.append(ip)
    for num in xrange(0,len(IP_list)):
        try:
        # bash equivalent: ping -c 1 > /dev/null
            sh.ping(IP_list[num], "-c 1 -i 0.2", _out="/dev/null")
            if Display_alive.lower()== "y":
                print "ping to", IP_list[num], "OK"
        except sh.ErrorReturnCode_1:
            print "no response from", IP_list[num]
    sys.exit()
def F5_scan():
    print "Opening F5 IP range file"
    with open("F5_Networks", 'r') as f:
        address=f.readlines()
    address=[x.strip('\n') for x in address]
    print "Opening F5 Gateway file"
    with open("F5_Gateways", 'r') as f:
        gateway_ips=f.readlines()
    gateway_ips=[x.strip('\n') for x in gateway_ips]
    IP_list=[]
    print "Generating list of IPs based off file"
    for i in xrange(0,len(address)):
        for ip in IPNetwork(address[i]):
            IP_list.append(ip)
    print "Scanning"
    for num in xrange(0,len(IP_list)):
        try:
     # bash equivalent: ping -c 1 > /dev/null
            sh.ping(IP_list[num], "-c 1 -i 0.2", _out="/dev/null")
        except sh.ErrorReturnCode_1:
            if IP_list[num] in gateway_ips:
                pass
            else:
                print "no response from", IP_list[num]
    sys.exit()
try:
    def main():
        args = sys.argv[1:]
        if not args:
            help()
        if sys.argv[1].lower() == "-m":
            F5_scan()
        if sys.argv[1].lower() == "-h" or sys.argv[1].lower() == "--help":
            help()
        if sys.argv[1].lower() == "-i" or sys.argv[1].lower() == "--ip":
            Display_alive = raw_input("Show hosts that are alive?(y/n): ")
            if Display_alive.lower() == "y" or Display_alive.lower() == "n":
                pass
            else:
                print "Invalid formatting try again"
                main()
            single_ip(Display_alive)
            if sys.argv[1].lower() == "-f" or sys.argv[1].lower() == "--file":
                Display_alive = raw_input("Show hosts that are alive?(y/n): ")
            if Display_alive.lower() == "y" or Display_alive.lower() == "n":
                pass
            else:
                print "Invalid formatting try again"
                main()
            file_scan(Display_alive)
        else:
            print "Invlaid formatting"
            sys.exit()
#check for ^C
except KeyboardInterrupt:
    print '\n'" Bye!"
    sys.exit()

#Call the main function
if __name__=='__main__':
    main()
    sys.exit()
