import socket
import dns.resolver
import requests
from bs4 import BeautifulSoup

def get_ip_addresses(domain):
    try:
        ip_addresses = socket.gethostbyname_ex(domain)
        return ip_addresses[2]
    except socket.gaierror:
        return []


def get_subdomains(domain):
    try:
        subdomains = []
        answers = dns.resolver.resolve(domain, "CNAME")
        for answer in answers:
            subdomains.append(answer.target.to_text()[:-1])
        return subdomains
    except dns.resolver.NXDOMAIN:
        return []
    except dns.resolver.NoAnswer:
        return []


def get_social_media_accounts(url):
    social_media_accounts = []

    # Example: Extracting Twitter accounts
    response = requests.get(f"https://twitter.com/{url}")
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        twitter_accounts = soup.select("a[data-testid='UserProfileHeader_Items']")
        for account in twitter_accounts:
            social_media_accounts.append(account.get("href"))

    # Add more scraping or API calls for other social media platforms

    return social_media_accounts


# Example usage
target_domain = "example.com"  # Enter the target domain

ip_addresses = get_ip_addresses(target_domain)
print(f"IP Addresses for {target_domain}:")
for ip_address in ip_addresses:
    print(ip_address)

subdomains = get_subdomains(target_domain)
print(f"\nActive Subdomains for {target_domain}:")
for subdomain in subdomains:
    if get_ip_addresses(subdomain):
        print(subdomain)

print(f"\nSocial Media Accounts for {target_domain}:")
for subdomain in subdomains:
    social_media_accounts = get_social_media_accounts(subdomain)
    for account in social_media_accounts:
        print(account)
