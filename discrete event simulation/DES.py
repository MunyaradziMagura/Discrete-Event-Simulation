import simpy
import random

#  generate the pipe 
def pipe_generator(env, start_temperature, start_vibration, limit_temperature, limit_vibration, sensor_interval_time, sensor):
    # which sensor is being simulated
    sensor_id = 0

    # because there are only three sensors
    while sensor_id < 3:
        #  create an instance of the water within the pipe
        water = sensor_generator(env, sensor_id,start_temperature, start_vibration, limit_temperature, limit_vibration, sensor)

        # run the water instance for this sensor i.e. simulate water running though this section of the pipe 
        env.process(water)

        # time until the next sensor is reached by water 
        time = random.expovariate(1.0 / sensor_interval_time)

        # create a new sensor when time has passed
        yield env.timeout(time)

        sensor_id += 1




# this function is the waters journey through the pipe 
def sensor_generator(env, sensor_id,start_temperature, start_vibration, limit_temperature, limit_vibration,sensor):
    pass

env.Enviroment()