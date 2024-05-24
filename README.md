# FaceFinder
<pre>
███████╗ █████╗  ██████╗███████╗    ███████╗██╗███╗   ██╗██████╗ ███████╗██████╗ 
██╔════╝██╔══██╗██╔════╝██╔════╝    ██╔════╝██║████╗  ██║██╔══██╗██╔════╝██╔══██╗
█████╗  ███████║██║     █████╗      █████╗  ██║██╔██╗ ██║██║  ██║█████╗  ██████╔╝
██╔══╝  ██╔══██║██║     ██╔══╝      ██╔══╝  ██║██║╚██╗██║██║  ██║██╔══╝  ██╔══██╗
██║     ██║  ██║╚██████╗███████╗    ██║     ██║██║ ╚████║██████╔╝███████╗██║  ██║
╚═╝     ╚═╝  ╚═╝ ╚═════╝╚══════╝    ╚═╝     ╚═╝╚═╝  ╚═══╝╚═════╝ ╚══════╝╚═╝  ╚═╝
A tool for searching domains, IPv4 and CIDR of companies by certificates
https://github.com/larinskiy/facefinder
Based on tools: cert.sh -> dns lookup -> whois
After program complete, check files out_domains.txt, out_ips.txt and out_cidrs.txt
</pre>

## Installation

`pip install -r requirements.txt` - install libraries for FaceFinder usage.

## Usage examples

`python facefinder.py` - run FaceFinder in interactive mode

`python facefinder.py -d <DOMAIN or COMPANY>` - perform search for specified domain name or company name

`python facefinder.py -dl <DOMAIN FILE>` - perform procedures for specified domain names in DOMAIN FILE

`python facefinder.py -il <IP FILE>` - perform CIDR search for specified IPs in IP FILE

`python facefinder.py -pd <PRIMARY DOMAIN NAME>` - perform all procedures and MX/NS request for specified PRIMARY DOMAIN NAME

## Installation

Output files are:

`domain_<DOMAIN or COMPANY>.txt` - list of domains with A records and without A records

`ip_<DOMAIN or COMPANY>.txt` - list of IPv4 address founded during nslookup procedures of domains

`cidrs_<DOMAIN or COMPANY>.txt` - list of CIDRs discovered during whois request for IPv4 addresses

## Bugs
If you find bugs in the operation of this program, be sure to let me know about them. This tool was developed spontaneously, but its support continues. Report bugs in this repository.