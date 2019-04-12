from pysoundio import (
    PySoundIo,
    SoundIoBackendWasapi,
    SoundIoFormatS16LE,
    SoundIoFormatFloat32LE,
)
from time import sleep
import sys

import numpy as np

class NumpyQueue:
    def __init__(self, max_length, channels=2, data=None):
        if data:
            self.data = np.array(data, dtype='int16')
        else:
            self.data = np.zeros((channels, max_length), dtype='int16')
        self.max_length = max_length
        self.channels = channels

    def length(self):
        return len(self.data)

    def append(self, value):
        self.data = np.concatenate((self.data, value), axis=1)
        # Trim the queue
        self.data = self.data[:, self.max_length * -1:]

    def read_last(self, length):
        return self.data[:, length * -1:]

    def pop_first(self, length):
        value = self.data[:, 0:length]
        self.data = self.data[:, length:]
        return value

import audioop
def get_level(data):
    rms = audioop.rms(data, 2) * 2
    level = float(rms) / (2 ** 16 / 2)
    normalize = 0
    if level != 0:
        dbs = 20 * np.log10(level)
        if np.isfinite(dbs):
            normalize = int(100 + dbs)
    return normalize

RUNNING = True
def error_callback(error):
    print(error)
    global RUNNING
    RUNNING = False

class PassThrough():
    def __init__(self):
        self.pysoundio = PySoundIo(backend=SoundIoBackendWasapi)
        self.read_queue = NumpyQueue(1024, 2)
        self.write_queue = None
        self.read_thread = None
        self.write_thread = None

    def start(self):
        channels = 2
        sample_rate = 48000
        block_size = 480

        in_device = self.pysoundio.get_default_input_device()
        in_device_dict = self.pysoundio.cast_device(in_device)
        in_frames_per_callback = int(in_device_dict['software_latency_current'] * sample_rate)

        for device in self.pysoundio.list_devices()[1]:
            if "Headphones".lower() in device['name'].lower() and not device['is_raw']:
                out_device = device
                break

        out_frames_per_callback = int(out_device['software_latency_current'] * sample_rate)
        frames_per_callback = max(out_frames_per_callback, in_frames_per_callback)

        self.write_queue = NumpyQueue(frames_per_callback * 2, 2)

        self.write_thread = self.pysoundio.start_output_stream(
            device_id=out_device['index'],
            channels=channels,
            sample_rate=sample_rate,
            block_size=block_size,
            dtype=SoundIoFormatS16LE,
            write_callback=self.write_callback,
            underflow_callback=self.underflow_callback,
            error_callback=error_callback
        )

        self.read_thread = self.pysoundio.start_input_stream(
            # device_id=9,
            channels=channels,
            sample_rate=sample_rate,
            block_size=block_size,
            dtype=SoundIoFormatS16LE,
            read_callback=self.read_callback,
            overflow_callback=self.overflow_callback,
            error_callback=error_callback
        )

    def overflow_callback(self):
        print("Overflow")

    def underflow_callback(self):
        print("Underflow")

    def read_callback(self, data, length):
        # print("read_callback")
        np_data = np.frombuffer(data, dtype="int16")
        np_data = np_data.reshape((2, -1))
        self.read_queue.append(np_data)
        read_data = self.read_queue.read_last(1024)
        audio_level = get_level(read_data.astype("int16").tostring())
        if audio_level > 0:
            self.write_queue.append(np_data)
        else:
            self.write_queue.append(np.zeros(np_data.shape, dtype="int16"))
        return

    def write_callback(self, data, length):
        # print("write_callback")
        np_data = self.write_queue.pop_first(length)
        buffer = np_data.astype("int16").tostring()
        if len(buffer) > 0:
            data[:] = buffer
        return data

    def stop(self):
        self.read_thread.stop()
        self.write_thread.stop()

    def __exit__(self):
        self.pysoundio.close()

if __name__ == '__main__':
    pass_through = PassThrough()
    print("Stream starting...")
    pass_through.start()
    print("Stream started")


    while RUNNING:
        try:
            sleep(1)
        except KeyboardInterrupt:
            RUNNING = False

    pass_through.stop()
    pass_through.pysoundio.close()
