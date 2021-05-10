# import

import simpy
from random import randint
print()
# config
TALKS_PER_SESSION = 3
TALK_LENGTH = 30
BREAK_LENGTH = 15
ATTENDEES = 3

# process function
def attendee(env, name, knowledge=0, hunger=0):
    talks = 0
    breaks = 0
    while True:
        # Visit talks
        for i in range(TALKS_PER_SESSION):
            knowledge += randint(0, 3) / (1 + hunger)
            hunger += randint(1, 4)
            talks += 1
            yield env.timeout(TALK_LENGTH)

        print('Attendee %s finished %d talks with knowledge %.2f and hunger %.2f.' % (name, talks, knowledge, hunger))

        # Go to buffet
        food = randint(3, 12)
        hunger -= min(food, hunger)
        breaks += 1

        yield env.timeout(BREAK_LENGTH)

        print('Attendee %s has finished break %d with hunger %.2f' % (name, breaks, hunger))

# setup environment and run simulation
env = simpy.Environment()
for i in range(ATTENDEES):
    env.process(attendee(env, i))
env.run(until=250)