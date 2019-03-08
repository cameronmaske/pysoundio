from pysoundio import (
    PySoundIo,
    SoundIoBackendWasapi,
    SoundIoFormatS16LE,
    SoundIoFormatFloat32LE,
)
from time import sleep 



class PassThrough():
    def __init__(self):
        self.pysoundio = PySoundIo(backend=SoundIoBackendWasapi)
        self.out_data = None 
    
    def start(self):
        channels = 2 
        sample_rate = 48000 
        block_size = 2048 

        in_device = self.pysoundio.get_default_input_device()
        out_device = self.pysoundio.get_default_output_device()

        self.pysoundio.start_output_stream(
            channels=channels,
            sample_rate=sample_rate,
            block_size=block_size,
            dtype=SoundIoFormatS16LE,
            # device_id=3,
            write_callback=self.write_callback,
            underflow_callback=self.underflow_callback
        )

        self.pysoundio.start_input_stream(
            # device_id=9,
            channels=channels,
            sample_rate=sample_rate,
            block_size=block_size,
            dtype=SoundIoFormatS16LE,
            # read_callback=self.read_callback
        )
    
    def underflow_callback(self):
        print("Underflow")

    def read_callback(self, data, length):
        print("Read: {}".format(length))
        # From the microphone
        self.out_data = data 

    def write_callback(self, data, length):
        # To the speakers
        if self.out_data:
            data[:] = self.out_data
        print("No out data")
        return data

    def __exit__(self): 
        self.pysoundio.close()

if __name__ == '__main__':
    pass_through = PassThrough()
    print("Stream starting...")
    pass_through.start()
    print("Stream started")

    try:
        while True:
            sleep(1)
    except KeyboardInterrupt:
        print('Exiting...')