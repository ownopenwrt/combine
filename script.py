import ipaddress
import requests
import re

TEXT_SOURCES = [
    "https://raw.githubusercontent.com/herrbischoff/country-ip-blocks/master/ipv4/ir.cidr",
    "https://www.ipdeny.com/ipblocks/data/countries/ir.zone",
]

IPHUB_SOURCE = "https://raw.githubusercontent.com/ownopenwrt/openwrt/main/iphub.txt"

CIDR_RE = re.compile(r'(\d+\.\d+\.\d+\.\d+/\d+)')

def normalize(cidr: str) -> str:
    return str(ipaddress.ip_network(cidr.strip(), strict=False))

def fetch_lines(url: str):
    r = requests.get(url, timeout=30)
    r.raise_for_status()
    return r.text.splitlines()

def main():
    result = set()

    # Sources with pure CIDR
    for url in TEXT_SOURCES:
        for line in fetch_lines(url):
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            result.add(normalize(line))

    # ip-hub mirror (mikrotik format)
    for line in fetch_lines(IPHUB_SOURCE):
        if line.startswith("#"):
            continue
        m = CIDR_RE.search(line)
        if m:
            result.add(normalize(m.group(1)))

    with open("iran_ip.lst", "w") as f:
        for cidr in sorted(result, key=lambda x: ipaddress.ip_network(x)):
            f.write(cidr + "\n")

if __name__ == "__main__":
    main()
