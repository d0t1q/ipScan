# ipScan Script
For the -m option to work you need to create two files 
F5_Gateways   F5_Networks

F5_Gateways contains the gateway and network ip (X.X.X.0 and X.X.X.255 -- Depends on subnet) these are IPs you want the scanner to ignore
F5_Networks contains the IP and netmask (X.X.X.0/24)


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
