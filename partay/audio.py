"""Audio related classes and functions."""

import audioop
from collections import deque
from collections.abc import Iterable
import math
import time

import numpy
import pyaudio


class Sampler(Iterable):
    """
    An iterable class reads samples from the system input device and yields
    the raw data.
    """

    default_rate = 44100
    default_width = 2
    default_channels = 2
    default_frames_per_buffer = 1024

    def __init__(self,
                 rate: int = default_rate,
                 width: int = default_width,
                 channels: int = default_channels,
                 frames_per_buffer: int = default_frames_per_buffer):
        self.pyaudio = pyaudio.PyAudio()

        self.rate = rate
        self.channels = channels
        self.width = width

        format = self.pyaudio.get_format_from_width(width)

        self.stream = self.pyaudio.open(
            format=format, channels=channels, rate=rate, input=True,
            output=False, frames_per_buffer=frames_per_buffer
        )

        self.frames_per_buffer = frames_per_buffer

    def __del__(self):
        self.stream.stop_stream()
        self.stream.close()

    def interpret_channels(self, sample_data, interleaved=True):
        if self.width == 1:
            data_type = numpy.uint8
        elif self.width == 2:
            data_type = numpy.int16
        else:
            raise ValueError('Only supports 8 and 16 bit audio formats.')

        channels = numpy.fromstring(sample_data, dtype=data_type)

        num_frames = self.frames_per_buffer

        if interleaved:
            # channels are interleaved, i.e. sample N of channel M follows sample N of channel M-1 in raw data
            channels.shape = (num_frames, self.channels)
            channels = channels.T
        else:
            # channels are not interleaved. All samples from channel M occur before all samples from channel M-1
            channels.shape = (self.channels, num_frames)

        return channels

    def __iter__(self):
        while self.stream.is_active():
            yield self.stream.read(self.frames_per_buffer)


class BeatDetector(Iterable):
    """
    An iterable which takes samples from a sampler and yields the detected
    beats.
    """

    default_window = 64
    default_cut_off_frequency = 80
    default_delay = 0.5

    def __init__(self,
                 sampler: Iterable,
                 cut_off_frequency: int = default_cut_off_frequency,
                 window: int = default_window,
                 delay: float = default_delay):
        self.sampler = sampler
        self.cut_off_frequency = cut_off_frequency
        self.buffer = deque(maxlen=window)
        self.delay = delay
        self.last_beat_time = None

    def running_mean(self, x, window_size):
        cumsum = numpy.cumsum(numpy.insert(x, 0, 0))
        return (cumsum[window_size:] - cumsum[:-window_size]) / window_size

    def filter_sample(self, sample_data):
        channels = self.sampler.interpret_channels(sample_data)

        frequency_ratio = self.cut_off_frequency / self.sampler.rate
        window_size = int(math.sqrt(0.196196 + frequency_ratio ** 2) / frequency_ratio)

        filtered = self.running_mean(channels[0], window_size).astype(channels.dtype)

        return filtered.tobytes('C')

    @property
    def energy_average(self):
        return numpy.average(self.buffer)

    @property
    def energy_variance(self):
        return numpy.var(self.buffer)

    @property
    def can_process_sample(self):
        if len(self.buffer) != self.buffer.maxlen:
            print(f'Waiting for buffer to fill... {len(self.buffer)}/{self.buffer.maxlen}')
            return False

        if self.last_beat_time is not None:
            if time.time() - self.last_beat_time <= self.delay:
                return False

        return True

    def __iter__(self):
        for unfiltered_sample in self.sampler:
            filtered_sample = self.filter_sample(unfiltered_sample)

            instant_energy = audioop.rms(filtered_sample, self.sampler.width)

            self.buffer.append(instant_energy)

            if not self.can_process_sample:
                continue

            c = -0.000025714 * self.energy_variance + 1.5142857

            threshold = self.energy_average * c

            #print(threshold, instant_energy)

            if instant_energy > threshold:
                self.last_beat_time = time.time()
                yield instant_energy


if __name__ == '__main__':
    sampler = Sampler()
    beat_detector = BeatDetector(sampler)

    for beat in beat_detector:
        bar = '#' * int(beat / 10)
        print(beat, bar)
