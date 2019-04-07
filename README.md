# loudsounds
listens for loud sounds and records them

add a delay so when a sound is heard it records
a minimum of like 10 to 20 seconds even if the sound stops

### notes to future self:
so future me knows what past me was thinking

* pass `device_index` to audiorecorder 

* it only opens one file per run, i want one file per detected
  loud noise, so we gotta do this `self.rec.open(args.filename, 'wb')`
  each time a noise is heard.

* move the save stuff to `soundDetected()` and `soundEnded()`
  and have those only trigger on sound start and sound end,
  this might be problematic tho since then the save delay would hold
  up `soundEnded()`

* `start_recording` will be called continuously
  while a loud noise plays, so I'll have check for state changes
  from quiet to loud then trigger `start_recording` and `stop_recording`


## Documentation:
an attempt at documenting what i write

**`find_input_device()`**

loops through all available devices and looks at the
name of the device, if the name has the word *mic* or *input* or *usb* in it
it'll select that device, so if you get stupid `device not found` errors
try adding keywords form the devices name in the list here: 
`for keyword in ["mic", "input", "usb"]:`