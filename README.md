manycast-dns
============

manycast-dns is a tool to simplify the parallel management of multiple cloud
anycast DNS providers.

Because even major anycast DNS providers with 100% uptime SLAs can suffer
outages, the only way to improve reliability is to spread your DNS over multiple
anycast networks. This tool is meant to provide a minimal command line interface
for provisioning and updating DNS across multiple cloud providers.

Dependencies / Supported clouds
-------------------------------

* [dnspython](https://pypi.python.org/pypi/dnspython)
* [boto3](https://pypi.python.org/pypi/boto3) / Amazon Web Services Route 53
* [google-cloud-dns](https://pypi.python.org/pypi/google-cloud-dns) / Google Cloud Platform DNS

Configuring
-----------

```
[google-cloud-platform]
; Google will provide this json file when creating an API user
json-credentials-file = config/google-cloud-credentials.json
project-id = principal-rhino-147203

[amazon-web-services]
access-key-id = ...
secret-access-key = ...
```

Example usage
-------------

```
# Provisioning Google Cloud from AWS
./manycast-dns provision whatbox.ca amazon-web-services google-cloud-platform

# Upserting SOA records
# These don't make a lot of sense with our approach, but they're still required. Each server must have any single valid server
# followed by an email with the @ replaced with a dot to contact, and various tuning parameters.
./manycast-dns upsert whatbox.ca whatbox.ca SOA 21600 "ns-1244.awsdns-27.org. servers.whatbox.ca. 1 7200 900 1209600 86400"
./manycast-dns upsert 192.131.44.0/24 192.131.44.0/24 SOA 21600 "ns-1131.awsdns-13.org. servers.whatbox.ca. 1 7200 900 1209600 86400"
./manycast-dns upsert 2620:B8:4000::/48 2620:B8:4000::/48 SOA 21600 "ns-97.awsdns-12.com. servers.whatbox.ca. 1 7200 900 1209600 86400"

# Upserting NS records
./manycast-dns upsert whatbox.ca whatbox.ca NS 172800 ns-1244.awsdns-27.org. ns-555.awsdns-05.net. ns-330.awsdns-41.com. ns-1936.awsdns-50.co.uk. ns-cloud-d1.googledomains.com. ns-cloud-d2.googledomains.com. ns-cloud-d3.googledomains.com. ns-cloud-d4.googledomains.com.
```
