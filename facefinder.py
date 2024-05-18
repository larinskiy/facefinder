import socket
from tqdm import tqdm
import ipwhois
import pandas as pd


def get_ipv4_addresses(domains):
    ipv4_addresses = set()
    for domain in tqdm(domains, desc=f"Searching IPv4", unit="domain"):
        try:
            ipv4_addresses = ipv4_addresses.union(
                set(socket.gethostbyname_ex(domain)[2]))
        except socket.gaierror:
            pass
    with open('out_ips.txt', 'w') as file:
        print(f'Number of detected IP addresses: {
              len(ipv4_addresses)}', file=file)
        print('IPs:\n', '\n'.join(ipv4_addresses), file=file)
    return sorted(ipv4_addresses)


def check_valid_domains(domains):
    validated = []
    for domain in tqdm(domains, desc=f"Validatiing domains", unit="domain"):
        try:
            socket.getaddrinfo(domain, 0, 0, 0, 0)
            validated.append(domain)
        except:
            pass
    with open('out_domains.txt', 'w') as file:
        print(f'Number of valid domains: {len(validated)}', file=file)
        print('Valid:\n', '\n'.join(validated), file=file)
    return validated


def get_cidrs(ipv4_addresses):
    subnets = set()
    keywords = input(
        "Enter the keywords separated by a space to search for ASN (For example, Amazon AZ): ").lower().split()
    for addr in tqdm(ipv4_addresses, desc=f"Searching CIDRs", unit="ip"):
        try:
            info = ipwhois.IPWhois(addr).lookup_whois()
            if any(keyword.lower() in info['asn_description'].lower() for keyword in keywords):
                subnets.add(net['asn_cidr'])
            else:
                for net in info['nets']:
                    if any(keyword.lower() in net['description'].lower() for keyword in keywords):
                        subnets.add(net['cidr'])
        except:
            pass
    with open('out_cidr.txt', 'w') as file:
        print(f'Number of subnets detected: {len(subnets)}', file=file)
        print('Subnets:\n', '\n'.join(subnets), file=file)
    return subnets


# Show logo, version, info
print('███████╗ █████╗  ██████╗███████╗    ███████╗██╗███╗   ██╗██████╗ ███████╗██████╗ \n\
██╔════╝██╔══██╗██╔════╝██╔════╝    ██╔════╝██║████╗  ██║██╔══██╗██╔════╝██╔══██╗\n\
█████╗  ███████║██║     █████╗      █████╗  ██║██╔██╗ ██║██║  ██║█████╗  ██████╔╝\n\
██╔══╝  ██╔══██║██║     ██╔══╝      ██╔══╝  ██║██║╚██╗██║██║  ██║██╔══╝  ██╔══██╗\n\
██║     ██║  ██║╚██████╗███████╗    ██║     ██║██║ ╚████║██████╔╝███████╗██║  ██║\n\
╚═╝     ╚═╝  ╚═╝ ╚═════╝╚══════╝    ╚═╝     ╚═╝╚═╝  ╚═══╝╚═════╝ ╚══════╝╚═╝  ╚═╝\n\
A tool for searching domains, IPv4 and CIDR of companies by certificates\n\
https://github.com/larinskiy/facefinder\n\n\
Based on tools: cert.sh -> dns lookup -> whois\n\n\
After program complete, check files out_domains.txt, out_ips.txt and out_cidrs.txt\n')


# Get subdomain set
comp = input(
    "Enter the company name to search for subdomains without spaces (For example, Amazon): ")
tables = pd.read_html(f"https://crt.sh/?q={comp}&exclude=expired&group=none")
domains = sorted(set(tables[2]["Common Name"]))

# Remove any whitespace characters from the domain names
domains = sorted(set([domain.strip() for domain in domains]))

# Check valid domains
validated = check_valid_domains(domains)

# Check if each domain exists
ipv4_addresses = get_ipv4_addresses(validated)

# Get CIDRs for company
get_cidrs(ipv4_addresses)
