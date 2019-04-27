# loudsounds
Script that listens for loud sounds and records them.

The idea is to put this on a pi and have it run overnight so I can finally
know how many drag races happen overnight.


## Documentation:
An attempt at documenting what I write

**CONSTANT variables:**

ok so I used a few constants, I'm lazy and I don't wanna wrap
the whole thing in another class.

variable name      |   what it does
-------------------|----------------------------------------------------------
FRAMES_PER_BLOCK   |   chunk size, calculated as RATE*INPUT_BLOCK_TIME
SHORT_NORMALIZE    |   used to normalize samples in the rms calculation to 1.0
OVERSENSITIVE      |   used to change sensitivity
UNDERSENSITIVE     |   also used to change sensitivity
RATE               |   audio sampling rate, change to your hardware's rate if you get audio speed issues

to find your hardware sample rate run this in your python shell:
``` python
import pyaudio
pa = pyaudio.PyAudio()
# change the index to the index of your soundcard
pa.get_device_info_by_index(0)['defaultSampleRate']
```


**`find_input_device()`:**

loops through all available devices and looks at the
name of the device, if the name has the word *mic* or *input* or *usb* in it
it'll select that device, so if you get stupid `device not found` errors
try adding keywords from the devices name in the list here:
`for keyword in ["mic", "input", "usb"]:`


**`record(duration)`:**

reads from the stream (`stream.read`) for `duration` seconds, and writes
whatever the stream returns to `wavefile`


**sensitivity:**

If a noise lasts 15 seconds or more `tap_threshold` gets multiplied by 1.1
If there is a 15 minute quiet stretch `tap_threshold` gets set back to its
initial value.
