# PPL redesign

RIght now what we have can be considered as a prototype. But the way that it is handling event is not the best way.

Make PPL into a library.



When they need a progress bar, they will create a pb object like

```python
from ppl import Pb

pb = Pb()
pb.start(total=100, task="Compute simulation")
```



The `Pb` class has an `__init__` function that will be used inorder to initialize someneeded values. This can actualy be changed per excecution with the use of `pb.update()`. Once they are updated, they remain updated, ie the changed that is made is not just for that single iteration but rather for all the coming iterations. `pb.update` can be used to change things like `total` or `task` etc.

> If `total` is not provided, we assume it to be a generator

But the main use of `pb.update` will be move the progressbar forward. We can also use a counter variable to make the progressbar skip a few steps. We can also reset a progressbar via `pb.update`.

```python
for i in range(100):
    // do stuff that takes tims
    pb.update(task="Simple loop", reset=False)
```

We can use the `task` + `reset` variables to make a new task run in the same progressbar, and just restarting it.

> `pb.update` can also have a message, that can be printed below or to the right of the task header



Now finally, once everything is done we can use `pb.complete` to finish off and clean up the mess or a pretty progressbar and put something like

```
(DONE) Task name <custom_message>
```

We can also provide a custom message inside `pb.complete`. The main use case of this that I have found will be for ML model training. We can get the output to look something like:

```
(DONE) Epoch 47  accuracy: 89.3% loss: 5%
```

The sytax for `pb.complete` is pretty simple. Just add a `pb.complete` at the end.

```python
pb.complete(message=f"accuracy: {accuracy}%  loss: {loss}%")
```



## Extra

We will also have a `pb.iter` which can be used like `tqdm`. We will still need a `pb.start` and `pb.complete` to clean things up. But you will not have to do stuff like `pb.update` every time. 



## Others

- cannot use the spinning thingy, will create issues when avg time is more than one second. Will probably have to use something like a sandclock icon or something static like that.

