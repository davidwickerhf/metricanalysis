import time
import logging

class Timer:
    def __init__(self, logger=None):
        self.start_time = None
        self.logger = logger or logging.getLogger(__name__)

    def start(self):
        self.start_time = time.time()
        self.logger.info("Timer started")

    def stop(self, task_name="Task"):
        if self.start_time is None:
            self.logger.warning("Timer was not started")
            return
        elapsed_time = time.time() - self.start_time
        self.logger.info(f"{task_name} completed in {elapsed_time:.2f} seconds")
        self.start_time = None