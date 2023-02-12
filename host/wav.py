# Plays a .wav file

import math
import struct
import pyaudio
import wave
import sys
import serial

if len(sys.argv) < 2:
    print("Plays a wave file.\n\nUsage: %s filename.wav" % sys.argv[0])
    sys.exit(-1)

CHUNK = 1024
PORT = 'COM3'
LED_COUNT = 138

count = LED_COUNT - 1

arduino = serial.Serial(port=PORT, baudrate=500000, timeout=.1)

def write(x):
    arduino.write(bytes(x, 'ascii'))

while True:
    p = pyaudio.PyAudio()
    wf = wave.open(sys.argv[1], 'rb')

    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)

    # Read data
    data = wf.readframes(CHUNK)


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
        stream.write(data)
        data = wf.readframes(CHUNK)
