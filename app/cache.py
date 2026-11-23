
"""Simple in-memory TTL cache for ChalanCheck RAG answers."""

import logging
import threading
import time
from collections import OrderedDict
from copy import deepcopy

logger = logging.getLogger("chalancheck.cache")

CACHE_TTL_SECONDS = 600
CACHE_MAX_ENTRIES = 100

_cache = OrderedDict()
_lock = threading.Lock()


def get_cached_answer(key: tuple) -> dict | None:
    """Return a valid cached answer, or None on a miss."""
    with _lock:
        entry = _cache.get(key)

        if entry is None:
            logger.info("RAG cache MISS")
            return None

        expires_at, result = entry

        if time.monotonic() >= expires_at:
            del _cache[key]
            logger.info("RAG cache EXPIRED")
            return None

        _cache.move_to_end(key)
        logger.info("RAG cache HIT")
        return deepcopy(result)


def set_cached_answer(key: tuple, result: dict) -> None:
    """Cache a successful grounded answer."""
    with _lock:
        _cache[key] = (
            time.monotonic() + CACHE_TTL_SECONDS,
            deepcopy(result),
        )
        _cache.move_to_end(key)

        while len(_cache) > CACHE_MAX_ENTRIES:
            _cache.popitem(last=False)


def clear_cache() -> None:
    """Clear cached answers, useful for tests."""
    with _lock:
        _cache.clear()
