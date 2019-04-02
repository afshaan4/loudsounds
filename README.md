# loudsounds
listens for loud sounds and records them

add a delay so when a sound is heard it records
a minimum of like 10 to 20 seconds even if the sound stops

### notes to future self:
so future me knows what past me was thinking

* added some saving logic to the main file, prolly wont work

* `start_recording` will be called continuously
while a loud noise plays, so I'll have check for state changes
from quite to loud then trigger `start_recording` and `stop_recording`


## Documentation:
an attempt at documenting what i write

**`find_input_device()`**

loops through all available devices and looks at the
name of the device, if the name has the word *mic* or *input* or *usb* in it
it'll select that device, so if you get stupid `device not found` errors
try adding keywords form the devices name in the list here: 
`for keyword in ["mic", "input", "usb"]:`