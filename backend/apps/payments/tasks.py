import logging

from celery import shared_task

logger = logging.getLogger(__name__)


@shared_task
def notify_payment_processed(payment_id: int) -> None:
    logger.info("Payment processed notification queued for payment_id=%s", payment_id)
