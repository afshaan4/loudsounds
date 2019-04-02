#!/usr/bin/python3

# stolen from here: https://stackoverflow.com/questions/4160175/detect-tap-with-pyaudio-from-live-mic
# modified to listen for loud stuff in general instead of just taps

import audiorecorder
import datetime
import argparse
import pyaudio
import struct
import math

# I know this is messy, some global vars here, some in the class
# fix it if ya want to
RATE = 44100  
INPUT_BLOCK_TIME = 0.05
FORMAT = pyaudio.paInt16 
SHORT_NORMALIZE = (1.0/32768.0)
INPUT_FRAMES_PER_BLOCK = int(RATE*INPUT_BLOCK_TIME)
# if we get this many noisy blocks in a row, increase the threshold
OVERSENSITIVE = 15.0/INPUT_BLOCK_TIME                    
# if we get this many quiet blocks in a row, decrease the threshold
UNDERSENSITIVE = 120.0/INPUT_BLOCK_TIME 


# handles cli arguments
parser = argparse.ArgumentParser(description = __doc__)
parser.add_argument(
    '-l', '--noise-length', type = int, default = 2/INPUT_BLOCK_TIME,
    help = 'max length of noise threshold, anything longer is ignored')
parser.add_argument(
    '-s', '--sensitivity', type = float, default = 0.010,
    help = 'sensitivity threshold, default is 0.010')
parser.add_argument(
    '-c', '--channels', type = int, default = 2,
    help = 'number of input channels')
parser.add_argument(
    'filename', nargs = '?', metavar = 'FILENAME',
    help = 'name of file to save recording in')
args = parser.parse_args()

if args.filename is None:
    cut = str(datetime.datetime.now())
    cut = cut.split()
    date = str(cut[0])
    time = str(cut[1])
    args.filename = ('yeet' + date + time + '.wav') 
    print(args.filename)
if args.noise_length:
    # length/blocksize, kinda like len(array) / len(array[0])
    args.noise_length = args.noise_length/INPUT_BLOCK_TIME


def get_rms( block ):
    # RMS amplitude is defined as the square root of the 
    # mean over time of the square of the amplitude.
    # so we need to convert this string of bytes into 
    # a string of 16-bit samples...

    # we will get one short out for each 
    # two chars in the string.
    count = len(block)/2
    format = "%dh"%(count)
    shorts = struct.unpack( format, block )

    # iterate over the block.
    sum_squares = 0.0
    for sample in shorts:
        # sample is a signed short in +/- 32768. 
        # normalize it to 1.0
        n = sample * SHORT_NORMALIZE
        sum_squares += n*n

    return math.sqrt( sum_squares / count )


class loudTester(object):
    def __init__(self):
        self.pa = pyaudio.PyAudio()
        self.stream = self.start_recording()
        self.rec = audiorecorder.Recorder(channels = 2)
        self.recfile = self.rec.open(args.filename, 'wb')
        self.tap_threshold = args.sensitivity
        self.noisycount = args.noise_length+1 
        self.quietcount = 0 
        self.errorcount = 0

    def find_input_device(self):
        device_index = None
        for i in range( self.pa.get_device_count() ):     
            devinfo = self.pa.get_device_info_by_index(i)   
            print( "Device %d: %s"%(i,devinfo["name"]) )

            # this stuff might change so if you get stupid
            # device not found issues, add a word from
            # your devices name in here(in lower case)
            for keyword in ["mic", "input", "usb"]:
                if keyword in devinfo["name"].lower():
                    print("Found an input: device %d - %s"%(i,devinfo["name"]))
                    device_index = i
                    return device_index

        if device_index == None:
            print( "No preferred input found; using default input device." )

        return device_index

    def start_recording( self ):
        device_index = self.find_input_device()

        stream = self.pa.open(  format = FORMAT,
                                channels = args.channels,
                                rate = RATE,
                                input = True,
                                input_device_index = device_index,
                                frames_per_buffer = INPUT_FRAMES_PER_BLOCK)
        return stream

    def soundDetected(self):
        print("YEET!+++++++++++++++++++")

    def soundEnded(self):
        print("NO U-------------------")

    def listen(self):
        try:
            block = self.stream.read(INPUT_FRAMES_PER_BLOCK)
        except IOError as e:
            # dammit. 
            self.errorcount += 1
            print( "(%d) Error recording: %s"%(self.errorcount,e) )
            self.noisycount = 1
            return

        amplitude = get_rms( block )
        print(amplitude)
        if amplitude > self.tap_threshold:
            # noisy block, start saving
            self.soundDetected()
            # TODO uncomment this
            self.recfile.start_recording()
            self.quietcount = 0
            self.noisycount += 1
            if self.noisycount > OVERSENSITIVE:
                # turn down the sensitivity
                self.tap_threshold *= 1.1
        else:            
            # quiet block, stop saving
            if 1 <= self.noisycount <= args.noise_length:
                self.soundEnded()
                # TODO uncomment this
                self.recfile.stop_recording()
            self.noisycount = 0
            self.quietcount += 1
            if self.quietcount > UNDERSENSITIVE:
                # turn up the sensitivity
                self.tap_threshold *= 0.9


if __name__ == "__main__":
    lt = loudTester()

    while True:
        lt.listen()