import socket
from tqdm import tqdm
import pandas as pd
import argparse
import os
from time import sleep
import dns.resolver
from googlesearch import search


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def get_first_domain(company_name):
    query = company_name
    for url in search(query, num=1, stop=1, pause=2):
        domain = url.split('//')[-1].split('/')[0]
        os.remove('./.google-cookie')
        return domain


def get_domains(company_name):
    print(f'[{bcolors.OKBLUE}i{bcolors.ENDC}] Perfoming request to Crt.sh for {
          company_name} ...')
    response = None
    while not response:
        try:
            response = pd.read_html(
                f"https://crt.sh/?q={company_name}&exclude=expired&group=none")
        except:
            print(f'[{bcolors.WARNING}!{
                bcolors.ENDC}] Crt.sh is unavailable. Trying again after 10 seconds...')
            sleep(10)
    print(f'[{bcolors.OKGREEN}+{bcolors.ENDC}] Got Crt.sh response')
    if response[1][1][0] != 'None found':
        identities = set()
        for record in set(response[2]["Matching Identities"]):
            identities = identities.union(record.split())
        domains = set(response[2]["Common Name"]).union(
            identities)
        print(f'[{bcolors.OKGREEN}+{bcolors.ENDC}] {len(domains)
                                                    } domain names successfully collected')
        return sorted(set([domain.strip() for domain in domains]))
    else:
        print(f'[{bcolors.WARNING}!{
            bcolors.ENDC}] No discovered certs on Crt.sh for {company_name}. Trying perform request for primary name...')
        global prime_domain
        if not args.primary_domain:
            prime_domain = input(f'[{bcolors.OKBLUE}?{bcolors.ENDC}] Primary domain name is set to {
                get_first_domain(comp)}. If it is valid, press enter. If not - enter valid primary domain: [For ex. amazon.com] ') or get_first_domain(company_name)
        else:
            prime_domain = args.primary_domain
        print(
            f'[{bcolors.OKGREEN}+{bcolors.ENDC}] Primary domain name is set to {prime_domain}')
        response = None
        while not response:
            try:
                response = pd.read_html(
                    f"https://crt.sh/?q={prime_domain}&exclude=expired&group=none")
            except:
                print(f'[{bcolors.WARNING}!{
                    bcolors.ENDC}] Crt.sh is unavailable. Trying again after 10 seconds...')
                sleep(10)
        print(f'[{bcolors.OKGREEN}+{bcolors.ENDC}] Got Crt.sh response')
        if response[1][1][0] != 'None found':
            identities = set()
            for record in set(response[2]["Matching Identities"]):
                identities = identities.union(record.split())
            domains = set(response[2]["Common Name"]).union(
                identities)
            print(f'[{bcolors.OKGREEN}+{bcolors.ENDC}] {len(domains)
                                                        } domain names successfully collected')
            return sorted(set([domain.strip() for domain in domains]).add(prime_domain))
        else:
            print(f'[{bcolors.WARNING}!{
                bcolors.ENDC}] No discovered certs on Crt.sh. Skipped domains verification')
            return set()


def get_records(domain, type):
    out_records = set()
    try:
        records = dns.resolver.resolve(domain, type)
        for record in records:
            if len(str(record).split(' ')) > 1:
                out_records.add(
                    str(record).split(' ')[-1])
            else:
                out_records.add(str(record))
        return out_records
    except Exception as e:
        return []


def get_ipv4_addresses(domains):
    ipv4_addresses = set()
    bar = tqdm(domains, desc=f"Searching IPv4", unit="domain")
    for domain in bar:
        try:
            ipv4_addresses = ipv4_addresses.union(
                set(socket.gethostbyname_ex(domain)[2]))
        except socket.gaierror:
            pass
        tqdm.set_postfix(bar, IPs=len(ipv4_addresses))
    if len(ipv4_addresses) != 0:
        ipv4_addresses = sorted(ipv4_addresses)
        with open(f'ips_{comp}.txt', 'w') as file:
            print(f'Number of detected IP addresses: {
                len(ipv4_addresses)}', file=file)
            print('IPs:\n', '\n'.join(ipv4_addresses), file=file)
            print(
                f'[{bcolors.OKGREEN}+{bcolors.ENDC}] Discovered IPs collected in ips_{comp}.txt')
    else:
        exit(f'[{bcolors.OKBLUE}i{bcolors.ENDC}] No discovered IPs')
    return sorted(ipv4_addresses)


def check_domains_records(domains):
    found_addr = []
    not_found_addr = []
    bar = tqdm(domains, desc=f"Checking records", unit="domain")
    for domain in bar:
        try:
            socket.getaddrinfo(domain, 0, 0, 0, 0)
            found_addr.append(domain)
        except:
            not_found_addr.append(domain)
        tqdm.set_postfix(bar, Records=len(found_addr),
                         NoRecords=len(not_found_addr))
    found_addr = sorted(found_addr)
    not_found_addr = sorted(not_found_addr)
    with open(f'domains_{comp}.txt', 'w') as file:
        print(f'Number of domains with addressess: {
              len(found_addr)}', file=file)
        print('Domain names:\n', '\n'.join(found_addr), file=file)
        print(f'Number of domains without addressess: {
              len(not_found_addr)}', file=file)
        print('Domain names:\n', '\n'.join(not_found_addr), file=file)
        print(
            f'[{bcolors.OKGREEN}+{bcolors.ENDC}] Results collected in domains_{comp}.txt')
    return found_addr


def get_cidrs(comp):
    response = None
    print(f'[{bcolors.OKBLUE}i{bcolors.ENDC}] Perfoming request to Bgp.he.net ...')
    while not response:
        try:
            response = pd.read_html(
                f"https://bgp.he.net/search?search%5Bsearch%5D={comp}&commit=Search")
        except:
            print(f'[{bcolors.WARNING}!{
                bcolors.ENDC}] Bgp.he.net is unavailable. Trying again after 10 seconds...')
            sleep(10)
    response = response[0]
    print(f'[{bcolors.OKGREEN}+{bcolors.ENDC}] Got Bgp.he.net repsonse')
    subnets = sorted(
        set(response[response['Type'].str.contains('Route')]['Result']))
    if len(subnets) != 0:
        with open(f'cidrs_{comp}.txt', 'w') as file:
            print(f'Number of subnets detected: {len(subnets)}', file=file)
            print('Subnets:\n', '\n'.join(subnets), file=file)
        print(f'[{bcolors.OKGREEN}+{bcolors.ENDC}] {len(subnets)
                                                    } CIDRs successfully collected')
        print(
            f'[{bcolors.OKGREEN}+{bcolors.ENDC}] Discovered CIDRs collected in cirds_{comp}.txt')
    else:
        print(f'[{bcolors.OKBLUE}i{bcolors.ENDC}] No discovered CIDRs')
    return subnets


# Show logo, version, info
print(f'{bcolors.HEADER}\
███████╗ █████╗  ██████╗███████╗    ███████╗██╗███╗   ██╗██████╗ ███████╗██████╗ \n\
██╔════╝██╔══██╗██╔════╝██╔════╝    ██╔════╝██║████╗  ██║██╔══██╗██╔════╝██╔══██╗\n\
█████╗  ███████║██║     █████╗      █████╗  ██║██╔██╗ ██║██║  ██║█████╗  ██████╔╝\n\
██╔══╝  ██╔══██║██║     ██╔══╝      ██╔══╝  ██║██║╚██╗██║██║  ██║██╔══╝  ██╔══██╗\n\
██║     ██║  ██║╚██████╗███████╗    ██║     ██║██║ ╚████║██████╔╝███████╗██║  ██║\n\
╚═╝     ╚═╝  ╚═╝ ╚═════╝╚══════╝    ╚═╝     ╚═╝╚═╝  ╚═══╝╚═════╝ ╚══════╝╚═╝  ╚═╝\n\
A tool for searching domains, IPv4 and CIDR of companies by company name\n\
https://github.com/larinskiy/facefinder{bcolors.ENDC}\n\n\
Based on tools: crt.sh -> dns lookup , bgp.he.net\n\n\
After program complete, check files domains.txt, ips.txt and cidrs.txt\n')

parser = argparse.ArgumentParser()
parser.add_argument(
    '--domain', '-d', help='Domain name for resource collecting')
parser.add_argument(
    '--domain-list', '-dl', help='Path to existing domain list (Do not request Crt.sh)')
parser.add_argument(
    '--primary-domain', '-pd', help='Perform NS and MX request for primary domain')
args = parser.parse_args()

# Get subdomain set
domains = set()
prime_domain = None
if not args.domain_list:
    if not args.domain:
        comp = input(
            f"[{bcolors.OKBLUE}?{bcolors.ENDC}] Enter the company name to search for domains without spaces (For example, Amazon): ")
    else:
        comp = args.domain
        print(f'[{bcolors.OKGREEN}+{bcolors.ENDC}] Company name set to {comp}')
    domains = domains.union(get_domains(comp))
elif os.path.isfile(args.domain_list):
    print(f'[{bcolors.OKGREEN}+{bcolors.ENDC}] Founded domain list file')
    with open(args.domain_list) as file:
        for record in file:
            domains = domains.union(record.strip())

# Perfom MX and NS search
if not prime_domain:
    if not args.primary_domain:
        prime_domain = input(f'[{bcolors.OKBLUE}?{bcolors.ENDC}] Primary domain name is set to {
            get_first_domain(comp)}. If it is valid, press enter. If not - enter valid primary domain: [For ex. amazon.com] ') or get_first_domain(comp)
    else:
        prime_domain = args.primary_domain
        print(
            f'[{bcolors.OKGREEN}+{bcolors.ENDC}] Primary domain name is set to {prime_domain}')
domains.add(prime_domain)
mx_domains = get_records(prime_domain, 'MX')
ns_domains = get_records(prime_domain, 'NS')
if len(mx_domains) != 0 or len(ns_domains) != 0:
    domains = set(mx_domains).union(set(ns_domains)).union(domains)
    print(f'[{bcolors.OKGREEN}+{bcolors.ENDC}] {len(mx_domains)} MX names and {
        len(ns_domains)} NS names was discovered')
else:
    print(f'[{bcolors.OKBLUE}i{bcolors.ENDC}] MX and NS records not found')

# Check domain records
if len(domains):
    found_addr = check_domains_records(domains)
else:
    print(f'[{bcolors.WARNING}!{
          bcolors.ENDC}] No discovered domains. Skipped checking domain records')
    found_addr = set()

# Check if each domain exists
if len(found_addr):
    ipv4_addresses = get_ipv4_addresses(found_addr)
else:
    print(f'[{bcolors.WARNING}!{
          bcolors.ENDC}] No discovered records. Skipped cheching IP addresses')

# Get CIDRs for company
get_cidrs(comp)
