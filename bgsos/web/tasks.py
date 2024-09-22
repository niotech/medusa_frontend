from celery import shared_task
from celery.utils.log import get_task_logger
import datetime

logger = get_task_logger(__name__)


@shared_task
def update_btc_payment_status():
    print(f"Task running at {datetime.datetime.now()}")
    logger.info("Info task is running.")
