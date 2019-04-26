# loudsounds
Script that listens for loud sounds and records them.

The idea is to put this on a pi and have it run overnight so I can finally
know how many drag races happen overnight.


## Documentation:
An attempt at documenting what I write

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