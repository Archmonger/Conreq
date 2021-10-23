from functools import partial
from time import time

import huey
from huey import Huey
from huey import crontab as _crontab
from huey.api import PeriodicTask, TaskWrapper
from huey.storage import SqliteStorage

from .consumer import FasterConsumer

# Ensure strict Huey crontabs
crontab = partial(_crontab, strict=True)
crontab.__doc__ = _crontab.__doc__
huey.crontab = crontab

# The time a task last ran
tasks_last_run = {}


class SqliteHuey(Huey):
    storage_class = SqliteStorage

    def create_consumer(self, **options):
        return FasterConsumer(self, **options)

    def periodic_task(
        self,
        crontab_or_seconds,
        retries=0,
        retry_delay=0,
        priority=None,
        context=False,
        name=None,
        expires=None,
        **kwargs,
    ):
        # Seconds
        if isinstance(crontab_or_seconds, int):

            def decorator(func):
                def method_validate(self, datetime):
                    function_name = str(self).split(": ")[0]
                    seconds = crontab_or_seconds

                    if not tasks_last_run.get(function_name):
                        tasks_last_run[function_name] = time()

                    if round(time() - tasks_last_run[function_name]) >= seconds:
                        tasks_last_run[function_name] = time()
                        return True

                    return False

                return TaskWrapper(
                    self,
                    func.func if isinstance(func, TaskWrapper) else func,
                    context=context,
                    name=name,
                    default_retries=retries,
                    default_retry_delay=retry_delay,
                    default_priority=priority,
                    default_expires=expires,
                    validate_datetime=method_validate,
                    task_base=PeriodicTask,
                    **kwargs,
                )

            return decorator

        # Crontab
        return super().periodic_task(
            crontab_or_seconds,
            retries=retries,
            retry_delay=retry_delay,
            priority=priority,
            context=context,
            name=name,
            expires=expires,
            **kwargs,
        )
