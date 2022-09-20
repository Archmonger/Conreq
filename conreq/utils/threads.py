"""Any function that assists in multithreading or multiprocessing"""
from dataclasses import dataclass, field
from threading import Thread
from typing import Any, Callable


@dataclass
class ThreadTask:
    func: Callable
    args: list = field(default_factory=list)
    kwargs: dict = field(default_factory=dict)


class ReturnThread(Thread):
    """Wrapper for python threads, however, these return a value."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._return = None

    def run(self):
        """
        The original run method does not return value after self._target is run.
        This child class added a return value.
        :return:
        """
        if self._target is not None:
            self._return = self._target(*self._args, **self._kwargs)

    def join(self, timeout: float | None = None) -> Any:
        """
        Join normally like the parent class, but added a return value which
        the parent class join method does not have.
        """
        super().join(timeout)
        return self._return


def executor(thread_tasks: list[ThreadTask]) -> list[Any]:
    """Threaded execution of a list of functions. Returns the results in the same
    order that the functions were provided in."""
    started_threads = []
    for task in thread_tasks:
        thread = ReturnThread(target=task.func, args=task.args, kwargs=task.kwargs)
        thread.start()
        started_threads.append(thread)

    return [thread.join() for thread in started_threads]
