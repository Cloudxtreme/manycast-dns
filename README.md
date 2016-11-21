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

* boto3 / Amazon Web Services Route 53
* google-cloud-dns / Google Cloud Platform DNS

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
# Provisioning google-cloud-platform from
./manycast-dns provision whatbox.ca amazon-web-services google-cloud-platform

# Upserting a record
./manycast-dns upsert whatbox.ca whatbox.ca NS 172800 ns-1244.awsdns-27.org. ns-555.awsdns-05.net. ns-330.awsdns-41.com. ns-1936.awsdns-50.co.uk. ns-cloud-d1.googledomains.com. ns-cloud-d2.googledomains.com. ns-cloud-d3.googledomains.com. ns-cloud-d4.googledomains.com.
```
