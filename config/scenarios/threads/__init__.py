"""
Thread-based parallel processing scenarios
هر ماژول شامل 3 سناریو است
"""

from . import (
    defining_thread,
    current_thread,
    thread_subclass,
    lock,
    rlock,
    semaphore,
    barrier
)

__all__ = [
    'defining_thread',
    'current_thread',
    'thread_subclass',
    'lock',
    'rlock',
    'semaphore',
    'barrier'
]
