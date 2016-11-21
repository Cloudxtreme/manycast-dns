# List of types supported across all implemented providers
SUPPORTED_TYPES = ['A', 'AAAA', 'NS', 'MX', 'SOA', 'TXT', 'CNAME', 'PTR']


def validate(name: str, type: str, ttl: int, values):
    if '/' in name:
        raise ValueError('name was presented in CIDR notation')

    if not name.endswith('.'):
        raise ValueError('name must end with a dot')

    if name.endswith('..'):
        raise ValueError('name should not end with two dots')

    if type in ['CNAME', 'PTR', 'NS']:
        for val in values:
            if not val.endswith('.'):
                raise ValueError(
                    'All values for type=%s must end with a .'
                    % type
                )
