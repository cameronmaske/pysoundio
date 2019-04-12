#
# Copyright (c) 2019 Joe Todd
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import sys
import platform
import os

__version__ = '1.1.0'

def is_win():
    return sys.platform.startswith("win")

def is_os_64bit():
    return platform.machine().endswith("64")


try:
    # Add library directory to path for Windows.
    if is_win():
        current_dir = os.path.dirname(os.path.abspath(__file__))
        bit = "x86"
        if is_os_64bit():
            bit = "x64"
        lib_path = os.path.join(current_dir, "./libs/win/%s/" % bit)
        os.environ["PATH"] += os.pathsep + lib_path
    import _soundiox as soundio
except ImportError as e:
    raise e
    sys.exit(-1)

from _soundiox import (
    SoundIoBackendNone, SoundIoBackendJack, SoundIoBackendPulseAudio,
    SoundIoBackendAlsa, SoundIoBackendCoreAudio, SoundIoBackendWasapi,
    SoundIoBackendDummy,
    SoundIoFormatS8, SoundIoFormatU8, SoundIoFormatS16LE,
    SoundIoFormatS16BE, SoundIoFormatU16LE, SoundIoFormatU16BE,
    SoundIoFormatS24LE, SoundIoFormatS24BE, SoundIoFormatU24LE,
    SoundIoFormatU24BE, SoundIoFormatS32LE, SoundIoFormatS32BE,
    SoundIoFormatU32LE, SoundIoFormatU32BE,
    SoundIoFormatFloat32LE, SoundIoFormatFloat32BE, SoundIoFormatFloat64LE,
    SoundIoFormatFloat64BE, SoundIoFormatInvalid
)
from .constants import (
    SoundIoBackend,
    SoundIoFormat
)
from .structures import (
    SoundIo,
    SoundIoChannelArea,
    SoundIoChannelLayout,
    SoundIoDevice,
    SoundIoInStream,
    SoundIoOutStream,
    SoundIoRingBuffer,
)
from .pysoundio import PySoundIo, PySoundIoError
