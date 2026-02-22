from __future__ import annotations

import random
import time
from dataclasses import dataclass
from typing import Callable, Iterable, Optional, TypeVar


T = TypeVar("T")


class TransientError(RuntimeError):
    """A retryable/transient error (network hiccup, rate limit, temporary IO, etc)."""


@dataclass(frozen=True)
class RetryConfig:
    max_attempts: int = 3
    base_delay_s: float = 0.5
    max_delay_s: float = 10.0
    jitter: bool = True


def _sleep_with_backoff(attempt_index: int, cfg: RetryConfig) -> float:
    # attempt_index: 0-based
    delay = min(cfg.base_delay_s * (2 ** attempt_index), cfg.max_delay_s)
    if cfg.jitter:
        delay = delay * (0.75 + random.random() * 0.5)  # 0.75x .. 1.25x
    time.sleep(delay)
    return delay


def with_retry(
    fn: Callable[[], T],
    *,
    cfg: RetryConfig = RetryConfig(),
    retry_on: Iterable[type[BaseException]] = (TransientError,),
) -> T:
    """
    Execute fn with exponential backoff retry.

    - Only retries exceptions in retry_on.
    - Raises the last exception if attempts exhausted.
    """
    last_err: Optional[BaseException] = None
    for attempt in range(cfg.max_attempts):
        try:
            return fn()
        except tuple(retry_on) as e:  # type: ignore[arg-type]
            last_err = e
            if attempt >= cfg.max_attempts - 1:
                raise
            _sleep_with_backoff(attempt, cfg)
    # should be unreachable
    assert last_err is not None
    raise last_err
