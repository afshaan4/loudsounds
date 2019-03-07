# loudsounds
listens for loud sounds and records them

changelog:

added some saving logic to the main file, prolly wont work
also `start_recording` will be called continuoisly
while a loud noise plays, so i'll have check for state changes
from quite to loud then trigger `start_recording` and `stop_recording`