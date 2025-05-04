from time import sleep

class CountDown:
    def __init__(self, start):
        self.start = start
    
    def __iter__(self):
        current = self.start
        while current > 0:
            yield current
            sleep(1)
            current -= 1

# Usage
countdown = CountDown(10)

for count in countdown:
    print(count)