# Plays PC sound

import math
import struct
import sys
import pyaudio
import serial

if len(sys.argv) < 2:
    print("Plays system sound.\n\nUsage: %s <volume multiplier>" % sys.argv[0])
    sys.exit(-1)

CHUNK = 1024
PORT = 'COM3'
LED_COUNT = 138

half = (LED_COUNT - 2) // 2

arduino = serial.Serial(port=PORT, baudrate=500000, timeout=.1)

def write(x):
    arduino.write(bytes(x, 'ascii'))

# Get volume of data
def rms(data):
    count = len(data) / 2
    format = "%dh" % (count)
    shorts = struct.unpack(format, data)
    sum_squares = 0.0
    for sample in shorts:
        n = sample * (1.0 / 32768)
        sum_squares += n * n
    return math.sqrt(sum_squares / count)

while True:
    p = pyaudio.PyAudio()

    stream = p.open(format=pyaudio.paInt16,
                channels=2,
                rate=44100,
                input=True,
                frames_per_buffer=CHUNK)

    # Read data
    data = stream.read(CHUNK)

    # Play the stream
    while len(data):
        write(str(math.floor((rms(data) * int(sys.argv[1])) * half)))
        data = stream.read(CHUNK)
