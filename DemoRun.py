from boat import Boat
from sensorTest import setup, cleanup, measure
import time
b = Boat()
setup()
d1 = 20
d2 = measure()
t = time.time()
t_n = time.time()
dt = t - t_n
while (dt < 120):
  while(d1 < 15 and d2 < 15):
    b.forward(200)
    time.sleep(0.1)
    d2 = measure()
  if (d1 < 15):
    b.left(200, 2)
  if (d2 < 15):
    b.right(200, 2)
  t_n = time.time()
cleanup()

