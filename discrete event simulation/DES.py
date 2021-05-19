import simpy
import random

#  generate the pipe 
def pipe_generator(env, start_temperature, start_vibration, limit_temperature, limit_vibration, sensor_interval_time, sensor):
    # which sensor is being simulated
    sensor_id = 0
    highest_temp = 0
    # because there are only three sensors
    while True and sensor_id < 3:
        
        # add the last temp to the new 
        if highest_temp > 0:
            start_temperature += highest_temp - start_temperature
        #  create an instance of the water within the pipe
        water = sensor_generator(env, sensor_id,start_temperature,highest_temp, start_vibration, limit_temperature, limit_vibration, sensor_interval_time,sensor)

        # run the water instance for this sensor i.e. simulate water running though this section of the pipe 
        env.process(water)

        # time until the next sensor is reached by water 
        time = random.expovariate(1.0 / sensor_interval_time)

        # create a new sensor when time has passed
        yield env.timeout(time, highest_temp)

        # incriment the sensors by 1
        sensor_id += 1


# this function is the waters journey through the pipe 
def sensor_generator(env, sensor_id,start_temperature,highest_temp, start_vibration, limit_temperature, limit_vibration, sensor_interval_time, sensor):
    
    # record the time the water starts changing tempreture at this sensor
    current_time = env.now
    print("Sensor:",sensor_id," started changing tempretures at",current_time," its current tempreture is ",start_temperature)
    
    temperature = start_temperature
    # request the sensor data
    with sensor.request() as req:
        # stop if no sensor is found 
        yield req

        # time left for the sensor
        sensor_time_left = env.now
        
        con_time = random.expovariate(1.0 / sensor_interval_time)
        
        while True:
            print("highest temp = ", highest_temp)
            interarrival = random.expovariate(sensor_id + 1)
            # if the temp reaches the pipe limit then we simulate the user manually lowering it
            if temperature > limit_temperature:
                temperature -= random.expovariate(1.0/interarrival) + (highest_temp / 3)
            else:
                temperature += random.expovariate(1.0/interarrival)
            # get the final tempreture 
            highest_temp = temperature
            
            # instead of yielding the arrival time, yield a Timeout Event
            yield env.timeout(interarrival,highest_temp)


            
            # to make things interesting, we add some printouts
            print( f'temp changed to {temperature:5.2f} Celsius at {env.now:5.2f}')
        
        yield env.timeout(con_time, highest_temp)
        



    # how fast it travles in cubic meters


# initlise the descrete event simulation enviroment
env = simpy.Environment()

sensor = simpy.Resource(env, capacity=1)

start_temperature = 24
start_vibration = 2
limit_temperature = 40
limit_vibration = 40
sensor_interval_time = 20

env.process(pipe_generator(env, start_temperature, start_vibration, limit_temperature, limit_vibration, sensor_interval_time, sensor))

env.run(until=60)