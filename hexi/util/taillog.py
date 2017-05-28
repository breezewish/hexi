import logging
import collections


log_queue = collections.deque(maxlen=500)


class TailLogHandler(logging.Handler):
  def __init__(self, log_queue):
    super().__init__()
    self.log_queue = log_queue

  def emit(self, record):
    self.log_queue.append(self.format(record))
