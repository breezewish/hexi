import asyncio
import logging

_subscribers = {}
_logger = logging.getLogger(__name__)


async def publish(key, value):
  _logger.debug('Event {0}'.format(key))
  coroutines = [subscriber({'key': key, 'value': value})
                for subscriber, key_set in _subscribers.items()
                if key in key_set]
  await asyncio.gather(*coroutines)


def subscribe(callback, keys):
  """Subscibe a set of event keys for a callback.

  Args:
    callback: coroutine function for event callback.
    keys: list, set or tuple of object for event keys.
  """
  assert type(keys) in (set, list, tuple)
  _subscribers[callback] = keys


def unsubscribe(callback):
  """Unsubscribe events for a callback.

  Args:
    callback: coroutine function for event callback.
  """
  if callback in _subscribers:
    del _subscribers[callback]
