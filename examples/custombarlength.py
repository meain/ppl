import time
from ppl import pb

for i in pb(range(100), bar_len=20):
    time.sleep(0.1)
