"""Conreq Thread Helper: Wrapper for python threads, however, these return a value."""

from threading import Thread


class ReturnThread(Thread):
    """Wrapper for python threads, however, these return a value."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._return = None  # child class's variable, not available in parent.

    def run(self):
        """
        The original run method does not return value after self._target is run.
        This child class added a return value.
        :return:
        """
        if self._target is not None:
            self._return = self._target(*self._args, **self._kwargs)

    def join(self, *args, **kwargs):
        """
        Join normally like the parent class, but added a return value which
        the parent class join method does not have.
        """
        super().join(*args, **kwargs)
        return self._return
