from huey.consumer import Consumer, Scheduler


class FasterScheduler(Scheduler):
    periodic_task_seconds = 1


class FasterConsumer(Consumer):
    scheduler_class = FasterScheduler
