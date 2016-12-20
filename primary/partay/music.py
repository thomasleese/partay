from threading import Thread

import numpy as np
import soundmeter.meter


class MyMeter(soundmeter.meter.Meter):
    """
    A customised sound meter which calls a function for each monitor event.
    Parameters
    ----------
    callback : function
        The callback function to be called.
    """

    def __init__(self, callback):
        super().__init__(self, segment=0.15)

        self.callback = callback

    def meter(self, rms):
        # override this method to stop printing
        pass

    def monitor(self, rms):
        self.callback(rms)


def listen(callback, threshold=350):
    readings = np.array([])

    def my_callback(rms):
        nonlocal readings

        readings = np.append(readings, rms)
        if len(readings) < 50:
            return

        readings = np.delete(readings, 0)

        average = np.mean(readings) + threshold
        maximum = np.max(readings) - average

        diff = rms - average
        if diff > 0:
            callback(diff / maximum)

    meter = MyMeter(my_callback)
    Thread(target=meter.start, daemon=True).start()
