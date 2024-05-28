# FaceFinder
<pre>
███████╗ █████╗  ██████╗███████╗    ███████╗██╗███╗   ██╗██████╗ ███████╗██████╗ 
██╔════╝██╔══██╗██╔════╝██╔════╝    ██╔════╝██║████╗  ██║██╔══██╗██╔════╝██╔══██╗
█████╗  ███████║██║     █████╗      █████╗  ██║██╔██╗ ██║██║  ██║█████╗  ██████╔╝
██╔══╝  ██╔══██║██║     ██╔══╝      ██╔══╝  ██║██║╚██╗██║██║  ██║██╔══╝  ██╔══██╗
██║     ██║  ██║╚██████╗███████╗    ██║     ██║██║ ╚████║██████╔╝███████╗██║  ██║
╚═╝     ╚═╝  ╚═╝ ╚═════╝╚══════╝    ╚═╝     ╚═╝╚═╝  ╚═══╝╚═════╝ ╚══════╝╚═╝  ╚═╝
A tool for searching domains, IPv4 and CIDR of companies by company name
https://github.com/larinskiy/facefinder
Based on tools: crt.sh -> dns lookup , bgp.he.net
After program complete, check files domains.txt, ips.txt and cidrs.txt
</pre>

## Installation

`pip install -r requirements.txt` - install libraries for FaceFinder usage.

## Usage examples

`python facefinder.py` - run FaceFinder in interactive mode

`python facefinder.py -d <COMPANY>` - perform search for specified COMPANY name

`python facefinder.py -dl <DOMAIN FILE>` - perform IP search for specified domain names in DOMAIN FILE

`python facefinder.py -pd <PRIMARY DOMAIN NAME>` - perform all procedures and MX/NS request for specified PRIMARY DOMAIN NAME

## Ouput files

Output files are:

`domain_<COMPANY>.txt` - list of domains with records, mask domains and without records

`ip_<COMPANY>.txt` - list of IPv4 address founded during nslookup procedures of domains

`cidrs_<COMPANY>.txt` - list of CIDRs discovered during whois request for IPv4 addresses

## Bugs
1. **No addresses found.**

Your firewall may block program requests to services required for validation. Before using the program, make sure that the firewall rules allow these requests. The program uses queries to Google services, DNS, Crt.sh and Bgp.he.net.

_If you find bugs in the operation of this program, be sure to let me know about them. This tool was developed spontaneously, but its support continues. Report bugs in this repository._