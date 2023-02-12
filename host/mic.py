# Plays microphone sound

import math
import struct
import pyaudio
import serial

CHUNK = 1024
PORT = 'COM3'
LED_COUNT = 138

count = LED_COUNT - 1

arduino = serial.Serial(port=PORT, baudrate=500000, timeout=.1)

def write(x):
    arduino.write(bytes(x, 'ascii'))

while True:
    p = pyaudio.PyAudio()

    stream = p.open(format=pyaudio.paInt16,
                channels=2,
                rate=44100,
                input=True,
                output=True,
                frames_per_buffer=CHUNK)

    # Read data
    data = stream.read(CHUNK)

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


    # Play the stream
    while len(data):
        write(str(math.floor((rms(data) * 2) * count)))
        data = stream.read(CHUNK)
