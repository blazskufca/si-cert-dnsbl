# si-cert-dnsbl

[SI-CERT](https://www.cert.si/informacije-za-zascito-sistemov/)'s phishing domain list (`misp/rpz/all.txt`) re-published as one domain per line, so DNS blocklist tools such as OPNsense Unbound DNSBL can read it.

- Entries from the last 365 days, deduplicated, lowercased, invalid names dropped
- Rebuilt daily at 02:17 UTC by GitHub Actions
- Blocklist URL: `https://raw.githubusercontent.com/blazskufca/si-cert-dnsbl/main/domains.txt`

The source data is freely accessible from SI-CERT; any use is the user's own responsibility. Report false positives to SI-CERT at cert@cert.si.
