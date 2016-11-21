import ipaddress
import re


# backported reverse_pointer support, can be removed when we drop support for
# < python 3.5
def bp_ip_address(address):
    try:
        return bp_ipv4_address(address)
    except (ipaddress.AddressValueError, ipaddress.NetmaskValueError):
        pass

    try:
        return bp_ipv6_address(address)
    except (ipaddress.AddressValueError, ipaddress.NetmaskValueError):
        pass

    raise ValueError('%r does not appear to be an IPv4 or IPv6 address' %
                     address)


class bp_ipv4_address(ipaddress.IPv4Address):
    @property
    def reverse_pointer(self):
        reverse_octets = str(self).split('.')[::-1]
        return '.'.join(reverse_octets) + '.in-addr.arpa'


class bp_ipv6_address(ipaddress.IPv6Address):
    @property
    def reverse_pointer(self):
        reverse_chars = self.exploded[::-1].replace(':', '')
        return '.'.join(reverse_chars) + '.ip6.arpa'


def is_ip(ip_address):
    try:
        bp_ip_address(ip_address).reverse_pointer
        return True
    except ValueError:
        return False


def ip_to_arpa(ip_address):
    return bp_ip_address(ip_address).reverse_pointer + '.'


def is_cidr(cidr):
    if '/' not in cidr:
        return False

    # TODO: check modulo, check format
    return True


def cidr_to_arpa(cidr):
    pieces = cidr.split('/')

    if int(pieces[1]) % 8 != 0:
        raise ValueError('No RFC 2317 support')

    ip = bp_ip_address(pieces[0])
    zone = ip.reverse_pointer

    trim_octets = int((ip.max_prefixlen - int(pieces[1])) / 8)
    for i in range(trim_octets):
        if ip.version == 4:
            # Remove one octet
            if zone[:2] != '0.':
                raise ValueErrror('Unexpected non-zero when removing octets')
            zone = zone[2:]
        elif ip.version == 6:
            # Remove two nibbles
            if zone[:4] != '0.0.':
                raise ValueErrror('Unexpected non-zero when removing nibbles')
            zone = zone[4:]

    return zone + '.'
