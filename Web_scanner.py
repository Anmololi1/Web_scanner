import socket
import dns.resolver
import requests
import re
from bs4 import BeautifulSoup
from tqdm import tqdm
from multiprocessing import Pool

def get_ip_addresses(domain):
    try:
        ip_addresses = dns.resolver.query(domain, "A")
        return ip_addresses
    except dns.resolver.NXDOMAIN:
        return []
    except dns.resolver.NoAnswer:
        return []


def get_subdomains(domain):
    try:
        subdomains = []
        answers = dns.resolver.query(domain, "ANY")
        for answer in answers:
            if answer.type == "CNAME":
                subdomains.append(answer.target.to_text()[:-1])
        return subdomains
    except dns.resolver.NXDOMAIN:
        return []
    except dns.resolver.NoAnswer:
        return []


def get_social_media_accounts(url):
    social_media_accounts = []

    # Example: Extracting Twitter accounts
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        twitter_accounts = soup.select("a[data-testid='UserProfileHeader_Items']")
        for account in twitter_accounts:
            social_media_accounts.append(account.get("href"))

    # Add more scraping or API calls for other social media platforms

    return social_media_accounts


# Example usage
target_domain = "example.com"  # Enter the target domain

with Pool(4) as pool:
    ip_addresses = pool.map(get_ip_addresses, subdomains)
    subdomains = pool.map(get_subdomains, subdomains)
    social_media_accounts = pool.map(get_social_media_accounts, subdomains)

print(f"IP Addresses for {target_domain}:")
for ip_address in ip_addresses:
    print(ip_address)

print(f"\nActive Subdomains for {target_domain}:")
for subdomain in subdomains:
    print(subdomain)

print(f"\nSocial Media Accounts for {target_domain}:")
for account in social_media_accounts:
    print(account)
