# Monkey patch Huey's filelock implementation to add Windows support.
import os
import sys


class FileLock:
    """Operating system agnostic file lock implementation using os.open and os.close."""

    def __init__(self, filename):
        self.filename = filename
        self.fd = None

        dirname = os.path.dirname(filename)
        if not os.path.exists(dirname):
            os.makedirs(dirname)
        elif os.path.exists(self.filename):
            os.unlink(self.filename)

    def acquire(self):
        flags = os.O_CREAT | os.O_TRUNC | os.O_RDWR
        self.fd = os.open(self.filename, flags)

    def release(self):
        if self.fd is not None:
            fd, self.fd = self.fd, None
            os.close(fd)

    def __enter__(self):
        self.acquire()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.release()


if sys.platform == "win32":
    import huey.utils

    huey.utils.FileLock = FileLock
