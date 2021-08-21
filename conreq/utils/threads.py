"""Any function that assists in multithreading or multiprocessing"""
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

    def join(self, timeout: int = None):
        """
        Join normally like the parent class, but added a return value which
        the parent class join method does not have.
        """
        super().join(timeout)
        return self._return


def threaded_execution(function_list: list, args: list, **kwargs: dict) -> list[any]:
    """Threaded execution of function calls where all functions utilize the same args/kwargs."""
    thread_list = []
    results = []

    for function in function_list:
        thread = ReturnThread(target=function, args=args, kwargs=kwargs)
        thread.start()
        thread_list.append(thread)

    for thread in thread_list:
        results.append(thread.join())

    return results


def threaded_execution_unique_args(functions: list[dict]) -> list[any]:
    """Executes functions with unique arguements. It will return all returned values as a list.
    Functions must follow this format:

        [{
            "function": foobar,
            "args": [],
            "kwargs": {},
            }, ...
        ]
    """
    thread_list = []
    for executable in functions:
        thread = ReturnThread(
            target=executable["function"],
            args=executable.get("args", None),
            kwargs=executable.get("kwargs", None),
        )
        thread.start()
        thread_list.append(thread)

    # Combine the results into one list
    results = []
    for index, thread in enumerate(thread_list):
        result = None
        try:
            result = thread.join()
        except:
            pass
        results.insert(index, result)

    return results
