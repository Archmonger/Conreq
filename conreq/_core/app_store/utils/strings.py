__license__ = "GNU Affero General Public License http://www.gnu.org/licenses/agpl.html"
__copyright__ = "Copyright (C) 2017 The OctoPrint Project - Released under terms of the AGPLv3 License"


def to_unicode(s_or_u, encoding="utf-8", errors="strict"):
    """
    Make sure ``s_or_u`` is a unicode string.
    Arguments:
        s_or_u (string or unicode): The value to convert
        encoding (string): encoding to use if necessary, see :meth:`python:bytes.decode`
        errors (string): error handling to use if necessary, see :meth:`python:bytes.decode`
    Returns:
        string: converted string.
    """
    if s_or_u is None:
        return s_or_u

    if isinstance(s_or_u, bytes):
        return s_or_u.decode(encoding, errors=errors)

    return str(s_or_u)


def to_native_str(s_or_u):
    """
    Make sure `s_or_u` is a native 'str' for the current Python version
    Will ensure a byte string under Python 2 and a unicode string under Python 3."""
    return to_unicode(s_or_u)
