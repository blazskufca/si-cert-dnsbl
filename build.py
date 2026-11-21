import datetime
import re
import sys
import time
import urllib.request

SOURCE = "https://www.cert.si/misp/rpz/all.txt"
MAX_AGE_DAYS = 365
MIN_DOMAINS = 100
DATE = re.compile(r"^\d{4}-\d{2}-\d{2}")
DOMAIN = re.compile(
    r"^(\*\.){,1}(([\da-zA-Z_])([_\w-]{,62})\.){,127}(([\da-zA-Z])[_\w-]{,61})"
    r"?([\da-zA-Z]\.((xn\-\-[a-zA-Z\d]+)|([a-zA-Z\d]{2,})))$"
)


def fetch(url, attempts=3):
    req = urllib.request.Request(url, headers={"User-Agent": "si-cert-dnsbl"})
    for attempt in range(1, attempts + 1):
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                return resp.read().decode()
        except OSError:
            if attempt == attempts:
                raise
            time.sleep(10 * attempt)


def domains(text, since):
    for line in text.splitlines():
        stamp, _, domain = line.strip().rpartition(",")
        domain = domain.strip().lower()
        if DATE.match(stamp) and stamp[:10] >= since and DOMAIN.match(domain):
            yield domain


def main(out):
    since = (datetime.date.today() - datetime.timedelta(days=MAX_AGE_DAYS)).isoformat()
    result = sorted(set(domains(fetch(SOURCE), since)))
    if len(result) < MIN_DOMAINS:
        sys.exit(f"only {len(result)} domains, keeping previous list")
    with open(out, "w") as f:
        f.write("\n".join(result) + "\n")
    print(f"{len(result)} domains since {since}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "domains.txt")
