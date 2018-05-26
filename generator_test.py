def square(nums):
    for i in nums:
        yield (i * i)


from progress import pb
import time

squares = square(range(150))
for i in pb(squares, task='Mapping Points'):
    time.sleep(.03)

squares = square(range(1000))
for i in pb(squares, task='Painting rainbow white'):
    time.sleep(.01)
