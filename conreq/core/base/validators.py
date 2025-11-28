import re

from django.core.validators import URLValidator
from django.utils.deconstruct import deconstructible
from django.utils.regex_helper import _lazy_re_compile


@deconstructible
class ExtendedURLValidator(URLValidator):
    """URL validator that supports hostnames (ex. https://sonarr:8000)"""

    # IP patterns
    ipv4_re = URLValidator.ipv4_re
    ipv6_re = URLValidator.ipv6_re
    hostname_re = URLValidator.hostname_re
    domain_re = URLValidator.domain_re
    tld_re = URLValidator.tld_re

    host_re = "(" + hostname_re + domain_re + tld_re + "|localhost|\w+)"

    regex = _lazy_re_compile(
        r"^(?:[a-z0-9.+-]*)://"  # scheme is validated separately
        r"(?:[^\s:@/]+(?::[^\s:@/]*)?@)?"  # user:pass authentication
        r"(?:" + ipv4_re + "|" + ipv6_re + "|" + host_re + ")"
        r"(?::[0-9]{1,5})?"  # port
        r"(?:[/?#][^\s]*)?"  # resource path
        r"\Z",
        re.IGNORECASE,
    )

    regex = _lazy_re_compile(
        r"^(?:[a-z0-9.+-]*)://"  # scheme is validated separately
        r"(?:[^\s:@/]+(?::[^\s:@/]*)?@)?"  # user:pass authentication
        r"(?:" + ipv4_re + "|" + ipv6_re + "|" + host_re + ")"
        r"(?::[0-9]{1,5})?"  # port
        r"(?:[/?#][^\s]*)?"  # resource path
        r"\Z",
        re.IGNORECASE,
    )
