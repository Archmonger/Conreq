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


def threaded_execution(function_list, args_list):
    """Threaded execution of function calls.
    Args:
        function_list: List containing references to functions
        args_list: List containing the arguments to be used for these function calls
    """
    thread_list = []
    results = []

    for function in function_list:
        thread = ReturnThread(
            target=function,
            args=args_list,
        )
        thread.start()
        thread_list.append(thread)

    for thread in thread_list:
        results.append(thread.join())

    return results
