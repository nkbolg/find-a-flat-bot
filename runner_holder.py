import logging
import signal

from threading import Event


class RunnerHolder:
    def __init__(self):
        self._stop = Event()
        signal.signal(signal.SIGINT, self.signal_handler)

    def wait(self, timeout_):
        logging.debug("waiting {} seconds".format(timeout_))
        ret = self._stop.wait(timeout_)
        logging.debug("RunnerHolder got {}".format(ret))
        return ret

    @property
    def stop_set(self):
        return self._stop.is_set()

    def signal_handler(self, sig, frame):
        logging.info('Signal: {}'.format(sig))
        logging.info('Stack: {}'.format(frame))
        logging.info('Ctrl+C pressed')
        self._stop.set()