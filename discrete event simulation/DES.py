import simpy
import random
import secrets
import csv 


    
# field names 
              # sensor 1
fields = ['time','sensor_one_temp','sensor_one_warning','sensor_one_alarm','sensor_one_emergency',
            'sensor_one_vib','sensor_one_warning_vib','sensor_one_alarm_vib','sensor_one_emergency_vib',
            # sensor 2
            'sensor_two_temp','sensor_two_warning','sensor_two_alarm','sensor_two_emergency',
            'sensor_two_temp_vib','sensor_two_warning_vib','sensor_two_alarm_vib','sensor_two_emergency_vib',
            # sensor 3 
            'sensor_three_temp','sensor_three_warning','sensor_three_alarm','sensor_three_emergency'
            ,'sensor_three_temp_vib','sensor_three_warning_vib','sensor_three_alarm_vib','sensor_three_emergency_vib']
# data rows of csv file 
rows = [] 
    
# name of csv file 
filename = "sensor_data.csv"

# for testing purpose, delete it pls
# temp_id = 0
# def identification(id):
#     return id

def identification(id):
    with open('id.txt', 'w') as f:
        f.write(f"{id}")
    return id

#  generate the pipe 
def pipe_generator(env, start_temperature, start_vibration, limit_temperature, limit_vibration, sensor_interval_time, sensor, warning_temp,warning_vib,rows):
    
    # which sensor is being simulated
    sensor_id = 0
    highest_temp = 0

    print("sensor1  | sensor2 | sensor3")

    # because there are only three sensors
    while True and sensor_id < 3:
        # set id
        identification(sensor_id)
        # print(f"\n\n\n\n\n\n\n\n{identification(sensor_id)}\n\n\n\n\n\n\n\n\n\n\n")
       
        csv_data = []
        # add the last temp to the new 
        if highest_temp > 0:
            start_temperature += highest_temp - start_temperature
        #  create an instance of the water within the pipe
        water = sensor_generator(env, sensor_id,start_temperature,highest_temp, start_vibration, limit_temperature, limit_vibration, sensor_interval_time, sensor, warning_temp,warning_vib)
        # water = sensor_generator(env,start_temperature,highest_temp, start_vibration, limit_temperature, limit_vibration, sensor_interval_time, sensor, warning_temp)

        # run the water instance for this sensor i.e. simulate water running though this section of the pipe 
        env.process(water)
        
        # time until the next sensor is reached by water 
        time = random.expovariate(1.0 / sensor_interval_time)
        # create a new sensor when time has passed
        yield env.timeout(time, highest_temp)
        rows.append(csv_data)
        
        # incriment the sensors by 1
        sensor_id += 1



# this function is the waters journey through the pipe 
def sensor_generator(env, sensor_id,start_temperature,highest_temp, start_vibration, limit_temperature, limit_vibration, sensor_interval_time, sensor, warning_temp,warning_vib):
# def sensor_generator(env, start_temperature, highest_temp, start_vibration, limit_temperature, limit_vibration, sensor_interval_time, sensor, warning_temp):
    
    # record the time the water starts changing tempreture at this sensor
    current_time = env.now
    # print("------Sensor:",sensor_id," started changing tempretures at", current_time," its current tempreture is ", start_temperature)
    
    # temperature 
    temperature = start_temperature
   
    new_id = int(open("id.txt", "r").read())

    # get the staring states of each sensor
    switch (new_id) {
        case 0:
            # set sensor one data
            sensor_one_data = [f'{temperature:5.2f} ',f'{vib_warning}',f'{temp_alerm}',f'{temp_emergency}',f'{vibration}',f'{vib_warning}',f'{vib_alerm}',f'{vib_emergency}']
            sensor_two_data = [f'{start_temperature}',f'{False}',f'{False}',f'{False}',f'{start_vibration}',f'{False}',f'{False}',f'{False}']
            sensor_three_data = [f'{start_temperature}',f'{False}',f'{False}',f'{False}',f'{start_vibration}',f'{False}',f'{False}',f'{False}']
            #append the data to the csv rows array
            rows.append(current_time + sensor_one_data + sensor_two_data + sensor_three_data)
            break;
        case 1:
            sensor_one_data = [f'{start_temperature}',f'{None}',f'{None}',f'{None}',f'{start_vibration}',f'{None}',f'{None}',f'{None}']
            sensor_two_data = [f'{temperature:5.2f} ',f'{vib_warning}',f'{temp_alerm}',f'{temp_emergency}',f'{vibration}',f'{vib_warning}',f'{vib_alerm}',f'{vib_emergency}']
            sensor_three_data = [f'{start_temperature}',f'{False}',f'{False}',f'{False}',f'{start_vibration}',f'{False}',f'{False}',f'{False}']
            rows.append(current_time + sensor_one_data + sensor_two_data + sensor_three_data)
            break;
        case 2:
            sensor_one_data = [f'{temperature:5.2f} ',f'{vib_warning}',f'{temp_alerm}',f'{temp_emergency}',f'{vibration}',f'{vib_warning}',f'{vib_alerm}',f'{vib_emergency}']
            sensor_two_data = [f'{start_temperature}',f'{None}',f'{None}',f'{None}',f'{start_vibration}',f'{None}',f'{None}',f'{None}']
            sensor_three_data = [f'{start_temperature}',f'{None}',f'{None}',f'{None}',f'{start_vibration}',f'{None}',f'{None}',f'{None}']
            rows.append(current_time + sensor_one_data + sensor_two_data + sensor_three_data)
            break;
    }
    # request the sensor data
    with sensor.request() as req:
        # print("sensor_id ", sensor_id)
        # stop if no sensor is found 
        # yield req
        con_time = random.expovariate(1.0 / sensor_interval_time)
        
        while True:
            # temperture alert conditions
            temp_warning = False
            temp_alerm = False
            temp_emergency = False

            # vibration alert conditions
            vib_warning = False
            vib_alerm = False
            vib_emergency = False

            # ensure the new id remains constant
            new_id = int(open("id.txt", "r").read())

            # random number generator
            interarrival = random.expovariate(new_id + 1)
            # simulate vibration spikes 
            vibration = secrets.randbelow(start_vibration)
            
            # ensure the vibration is always above 0
            while vibration == 0:
                vibration = secrets.randbelow(start_vibration)

            # limit temperture from running away
            if temperature > limit_temperature:
                print("pipe temperture limit reached")
                temperature -= random.expovariate(1.0/interarrival) + (highest_temp / 3)
            else:
                temperature += random.expovariate(1.0/interarrival)
            
            # [warning, alerm, emergency]

            # catch vibration alerts
            if temperature > warning_temp[0]:
                temp_warning = True
                if temperature > warning_temp[1]:
                    temp_alerm = True
                    if temperature > warning_temp[2]:
                        temp_emergency = True
            
            # catch vibration alerts
            if vibration > warning_vib[0]:
                vib_warning = True
                if vibration > warning_vib[1]:
                    vib_alerm = True
                    if vibration > warning_vib[2]:
                        vib_emergency = True

            # get the final tempreture 
            highest_temp = temperature

            # get current time into an array
            print(f"current_time {env.now:5.2f} |" ,end="")
            time = [f"{env.now:5.2f}"]
            if new_id == 0:
                print( f' temp changed to {temperature:5.2f} degree/s Celsius at {env.now:5.2f} min/s || vibrated by {vibration} cubic meters |', end="")
                print("N/A   |", end="")  # sensor id = 1
                print("N/A")  # sensor id = 2

                # time, warnings
                # set sensor one data
                sensor_one_data = [f'{temperature:5.2f} ',f'{vib_warning}',f'{temp_alerm}',f'{temp_emergency}',f'{vibration}',f'{vib_warning}',f'{vib_alerm}',f'{vib_emergency}']
                sensor_two_data = [f'{start_temperature}',f'{False}',f'{False}',f'{False}',f'{start_vibration}',f'{False}',f'{False}',f'{False}']
                sensor_three_data = [f'{start_temperature}',f'{False}',f'{False}',f'{False}',f'{start_vibration}',f'{False}',f'{False}',f'{False}']
                #append the data to the csv rows array
                rows.append(time + sensor_one_data + sensor_two_data + sensor_three_data)
            elif new_id == 1:
                print("N/A   |", end="")  # sensor id = 0
                print( f' temp changed to {temperature:5.2f} degree/s Celsius at {env.now:5.2f} min/s || vibrated by {vibration} cubic meters |', end="")
                print("N/A   |")  # sensor id = 2
                sensor_one_data = [f'{start_temperature}',f'{None}',f'{None}',f'{None}',f'{start_vibration}',f'{None}',f'{None}',f'{None}']
                sensor_two_data = [f'{temperature:5.2f} ',f'{vib_warning}',f'{temp_alerm}',f'{temp_emergency}',f'{vibration}',f'{vib_warning}',f'{vib_alerm}',f'{vib_emergency}']
                sensor_three_data = [f'{start_temperature}',f'{False}',f'{False}',f'{False}',f'{start_vibration}',f'{False}',f'{False}',f'{False}']
                rows.append(time + sensor_one_data + sensor_two_data + sensor_three_data)
            elif new_id == 2:
                print("N/A   |", end="")  # sensor id = 0
                print("N/A   |", end="")  # sensor id = 1
                print( f' temp changed to {temperature:5.2f} degree/s Celsius at {env.now:5.2f} min/s || vibrated by {vibration} cubic meters |')  
                sensor_one_data = [f'{temperature:5.2f} ',f'{vib_warning}',f'{temp_alerm}',f'{temp_emergency}',f'{vibration}',f'{vib_warning}',f'{vib_alerm}',f'{vib_emergency}']
                sensor_two_data = [f'{start_temperature}',f'{None}',f'{None}',f'{None}',f'{start_vibration}',f'{None}',f'{None}',f'{None}']
                sensor_three_data = [f'{start_temperature}',f'{None}',f'{None}',f'{None}',f'{start_vibration}',f'{None}',f'{None}',f'{None}']
                rows.append(time + sensor_one_data + sensor_two_data + sensor_three_data)

            # instead of yielding the arrival time, yield a Timeout Event
            yield env.timeout(interarrival,highest_temp)




# notifications need to be in diffenrt tables
# data can be generated in sec or min

# initlise the descrete event simulation enviroment
env = simpy.Environment()

sensor = simpy.Resource(env, capacity=1)

start_temperature = 24
# [warning, alerm, emergency]
warning_temp = [37, 38, 39]
warning_vib = [3, 6, 9]
start_vibration = 10
limit_temperature = 40
limit_vibration = 1
sensor_interval_time = 20

# store the last temp of a sensor

env.process(pipe_generator(env, start_temperature, start_vibration, limit_temperature, limit_vibration, sensor_interval_time, sensor, warning_temp,warning_vib,rows))

env.run(until=60)


# writing to csv file 
with open(filename, 'w') as csvfile: 
    # creating a csv writer object 
    csvwriter = csv.writer(csvfile) 
    # writing the fields 
    csvwriter.writerow(fields) 
    # writing the data rows 
    csvwriter.writerows(rows)