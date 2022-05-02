__license__ = "GNU Affero General Public License http://www.gnu.org/licenses/agpl.html"
__copyright__ = "Copyright (C) 2017 The OctoPrint Project - Released under terms of the AGPLv3 License"

import sys

try:
    import fcntl
except ImportError:
    fcntl = None

# set_close_exec

if fcntl is not None and hasattr(fcntl, "FD_CLOEXEC"):

    def set_close_exec(handle):
        """Set ``close_exec`` flag on handle, if supported by the OS."""
        flags = fcntl.fcntl(handle, fcntl.F_GETFD)
        flags |= fcntl.FD_CLOEXEC
        fcntl.fcntl(handle, fcntl.F_SETFD, flags)

elif sys.platform == "win32":

    def set_close_exec(handle):
        """Set ``close_exec`` flag on handle, if supported by the OS."""
        import ctypes
        import ctypes.wintypes

        # see https://msdn.microsoft.com/en-us/library/ms724935(v=vs.85).aspx
        SetHandleInformation = ctypes.windll.kernel32.SetHandleInformation
        SetHandleInformation.argtypes = (
            ctypes.wintypes.HANDLE,
            ctypes.wintypes.DWORD,
            ctypes.wintypes.DWORD,
        )
        SetHandleInformation.restype = ctypes.c_bool

        HANDLE_FLAG_INHERIT = 0x00000001

        result = SetHandleInformation(handle, HANDLE_FLAG_INHERIT, 0)
        if not result:
            raise ctypes.GetLastError()

else:

    def set_close_exec(_):
        """Set ``close_exec`` flag on handle, if supported by the OS."""
        # no-op
        pass


CLOSE_FDS = sys.platform != "win32" or sys.version_info >= (3, 7)
"""
Default setting for close_fds parameter to Popen/sarge.run.
Set ``close_fds`` on every sub process to this to ensure file handlers will be closed
on child processes on platforms that support this (anything Python 3.7+ or anything
but win32 in earlier Python versions).
"""

_OPERATING_SYSTEMS = {
    "windows": ["win32"],
    "linux": lambda x: x.startswith("linux"),
    "macos": ["darwin"],
    "freebsd": lambda x: x.startswith("freebsd"),
}
OPERATING_SYSTEM_UNMAPPED = "unmapped"


def get_os():
    """
    Returns a canonical OS identifier.
    Currently the following OS are recognized: ``win32``, ``linux`` (``sys.platform`` = ``linux*``),
    ``macos`` (``sys.platform`` = ``darwin``) and ``freebsd`` (``sys.platform`` = ``freebsd*``).
    Returns:
            (str) mapped OS identifier
    """
    return next(
        (
            identifier
            for identifier, platforms in _OPERATING_SYSTEMS.items()
            if (callable(platforms) and platforms(sys.platform))
            or (isinstance(platforms, list) and sys.platform in platforms)
        ),
        OPERATING_SYSTEM_UNMAPPED,
    )
