from ppl import pb
import time


for i in pb(range(10), mini=True):
    time.sleep(1)

for i in pb(range(10)):
    time.sleep(1)
