from celery import shared_task


@shared_task
def noop_healthcheck_task() -> str:
    return "ok"
