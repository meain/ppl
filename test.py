def square(nums):
    for i in nums:
        yield (i * i)


from progress import pb
import time

squares = square(range(150))
for i in pb(squares, task='Mapping Points'):
    time.sleep(.01)

squares = square(range(100))
for i in pb(squares, task='Painting rainbow white'):
    time.sleep(.05)
