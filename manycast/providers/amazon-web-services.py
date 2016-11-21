import collections
# import typing

import boto3


class DNS:
    def __init__(self, config, zone_name):
        self._client = boto3.client(
            'route53',
            aws_access_key_id=config['access-key-id'],
            aws_secret_access_key=config['secret-access-key']
        )
        self._zone_name = zone_name

        for zone_page in self._client.get_paginator('list_hosted_zones').paginate():
            for zone in zone_page['HostedZones']:
                if zone['Name'] == self._zone_name:
                    self._zone = zone['Id']

    # values will be a typing.List[str]
    def upsert(self, name: str, type: str, ttl: int, values):
        self._update('UPSERT', name, type, ttl, values)

    def delete(self, name: str, type: str, ttl: int, values):
        self._update('DELETE', name, type, ttl, values)

    def _update(self, mode: str, name: str, type: str, ttl: int, values):
        records = []
        for value in values:
            records.append({
                'Value': value,
            })

        response = self._client.change_resource_record_sets(
            HostedZoneId=self._zone,
            ChangeBatch={
                'Changes': [{
                    'Action': mode,
                    'ResourceRecordSet': {
                        'Name': name,
                        'Type': type,
                        'TTL': ttl,
                        'ResourceRecords': records,
                    }
                }]
            }
        )

    def list(self):
        Record = collections.namedtuple(
            'Record',
            ['name', 'type', 'ttl', 'values']
        )

        for record_page in self._client.get_paginator('list_resource_record_sets').paginate(
            HostedZoneId=self._zone
        ):
            for record in record_page['ResourceRecordSets']:
                values = []
                for valrec in record['ResourceRecords']:
                    values.append(valrec['Value'])

                # if record['Type'] in ['PTR', 'CNAME', 'NS']:
                #     values = [v if v.endswith('.') else v + '.' for v in values]

                yield Record(
                    name=record['Name'],
                    type=record['Type'],
                    ttl=record['TTL'],
                    values=values
                )
