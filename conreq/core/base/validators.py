import re

from django.core.validators import URLValidator
from django.utils.deconstruct import deconstructible
from django.utils.regex_helper import _lazy_re_compile


@deconstructible
class ExtendedURLValidator(URLValidator):
    """URL validator that supports hostnames (ex. https://sonarr:8000)"""

    # pylint: disable=too-few-public-methods
    ul = URLValidator.ul
    ipv4_re = URLValidator.ipv4_re
    ipv6_re = URLValidator.ipv6_re
    hostname_re = URLValidator.hostname_re
    domain_re = URLValidator.domain_re

    tld_re = (
        r"\.?"  # OPTIONAL dot (allows for hostnames)
        r"(?!-)"  # can't start with a dash
        r"(?:[a-z" + ul + "-]{2,63}"  # domain label
        r"|xn--[a-z0-9]{1,59})"  # or punycode label
        r"(?<!-)"  # can't end with a dash
        r"\.?"  # may have a trailing dot
    )

    host_re = "(" + hostname_re + domain_re + tld_re + "|localhost)"

    regex = _lazy_re_compile(
        r"^(?:[a-z0-9.+-]*)://"  # scheme is validated separately
        r"(?:[^\s:@/]+(?::[^\s:@/]*)?@)?"  # user:pass authentication
        r"(?:" + ipv4_re + "|" + ipv6_re + "|" + host_re + ")"
        r"(?::\d{2,5})?"  # port
        r"(?:[/?#][^\s]*)?"  # resource path
        r"\Z",
        re.IGNORECASE,
    )
