# pb

The progress bar library that stated with the idea of looking pretty.

> By default the bar length is the full width of the terminal window

## Installation

For now just put the `progress.py` in your project.

## How to use

### Simple usage

```
import time
from progress import pb

for i in pb(range(100)):
    time.sleep(0.1)
```

### Show task name along with the progress bar

```
import time
import random
from progress import pb

total = 120
tasks = [
    'Make paintball', 'Find dragons', 'Code in python', 'Take out the trash',
    'Fill up water bottles for trip'
]
for task in tasks:
    i = 0
    for i in pb(range(total), task=task):
        sleep_time = [.05, .04, .03, .02, .01][random.randint(0, 4)]
        time.sleep(sleep_time)  # emulating long-playing task
```

### Custom bar length
```
import time
from progress import pb

for i in pb(range(100)):
    time.sleep(0.1)
```
