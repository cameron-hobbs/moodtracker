import logging
import time

from django.core.cache import cache


logger = logging.getLogger("tracker")


def acquire_lock_blocking(cache_key):
    while True:
        if cache.add(cache_key, True, 60):
            break

        time.sleep(1)

    logger.info("Acquired lock")
