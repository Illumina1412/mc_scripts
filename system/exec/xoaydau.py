import minescript as m
import time
# Get current player position and rotation

while True:
    m.player_set_orientation(-180, -59)
    time.sleep(0.7)
    m.player_set_orientation(-180, -59.1)
