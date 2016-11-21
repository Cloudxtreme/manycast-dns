import collections
import time
# import typing

from google.cloud.dns import Client


class DNS:
    def __init__(self, config, zone_name):
        self._zone_name = zone_name

        real_client = client = Client.from_service_account_json(
            config['json-credentials-file'],
            project=config['project-id'])

        for zone in client.list_zones():
            if zone.dns_name == self._zone_name:
                self._zone = zone.name

        self._client = real_client.zone(self._zone)

    # values will be a typing.List[str]
    def upsert(self, name: str, type: str, ttl: int, values):
        record = self._client.resource_record_set(name, type, ttl, values)
        changes = self._client.changes()

        # Check if it already exists, and delete
        # We can get away with this because the delete and create are batched
        # together into one atomic operation.
        for entry in self.list():
            if name == entry.name and type == entry.type:
                old_record = self._client.resource_record_set(*entry)
                changes.delete_record_set(old_record)

        changes.add_record_set(record)
        changes.create()
        while changes.status != 'done':
            time.sleep(1)     # or whatever interval is appropriate
            changes.reload()   # API request

    def delete(self, name: str, type: str, ttl: int, values):
        record = self._client.resource_record_set(name, type, ttl, values)
        changes = self._client.changes()
        changes.delete_record_set(record)
        changes.create()
        while changes.status != 'done':
            time.sleep(1)     # or whatever interval is appropriate
            changes.reload()   # API request

    def list(self):
        Record = collections.namedtuple(
            'Record',
            ['name', 'type', 'ttl', 'values']
        )

        for record in self._client.list_resource_record_sets():
            yield Record(
                name=record.name,
                type=record.record_type,
                ttl=record.ttl,
                values=record.rrdatas
            )

    def nameservers(self):
        return self._client.name_servers
