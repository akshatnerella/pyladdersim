# Test script for PLC timers

import time
from pyladdersim.components import OnDelayTimer, OffDelayTimer, PulseTimer

# Initialize timers
ton = OnDelayTimer(name="TON", delay=5)
tof = OffDelayTimer(name="TOF", delay=5)
tp = PulseTimer(name="TP", delay=3)

# Simulate each timer in action
for i in range(10):
    print(f"Time: {i}")
    ton.update(i >= 2)  # TON input ON at t=2
    tof.update(i < 5)   # TOF input OFF at t=5
    tp.update(i == 2)   # TP input pulse at t=2

    print(f"  ON-Delay Timer (TON) state: {'ON' if ton.state else 'OFF'}")
    print(f"  OFF-Delay Timer (TOF) state: {'ON' if tof.state else 'OFF'}")
    print(f"  Pulse Timer (TP) state: {'ON' if tp.state else 'OFF'}\n")

    time.sleep(1)