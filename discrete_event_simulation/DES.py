import simpy
import random
import secrets
import csv
import os
# stores all the file functions
import files

# field names for csv
# sensor 1
fields = ['sensor(pk)', 'time(pk)','temperature','vibration']
alarm_feilds = ['sensor(pk)', 'time(pk)','temp_alert','vib_alert','temp_warning','vib_warning','temp_emergency','vib__emergency']

# data rows of csv file
rows = []
alarm_rows = []

# name of csv file
filename = "sensor_data.csv"
alarm_file = 'alarm.csv'

# write the id to an external text file for storage and dataloss prevention


#  generate the pipe
def pipe_generator(env, start_temperature, start_vibration, limit_temperature, limit_vibration, single_sensor_runtime, sensor, warning_temp, warning_vib, rows):

    # inilise which sensor is being simulated & what is the highest temp
    sensor_id = 0
    highest_temp = 0

    # print for clearity when looking at terminal output
    print('sensor_number', 'time', 'value','sensor_type','alert','warning','emergency')

    # because there are only three sensors
    while True and sensor_id < int(files.get_sensor()):

        # set id
        files.set_sensor_id(sensor_id)
        
        # store csv data into this array for each sensor
        csv_data = []

        # add the last temp to the new
        if highest_temp > 0:

            # update stating temp
            start_temperature += highest_temp - start_temperature

        #  create an instance of the pipe_activity within the pipe
        pipe_activity = sensor_generator(env, start_temperature, highest_temp, start_vibration,
                                 limit_temperature, limit_vibration, single_sensor_runtime, sensor, warning_temp, warning_vib)

        # run the pipe_activity instance for this sensor i.e. simulate pipe_activity running though this section of the pipe
        env.process(pipe_activity)

        # time until the next sensor is reached by pipe_activity
        time = random.expovariate(1.0 / single_sensor_runtime)
        # create a new sensor when time has passed
        yield env.timeout(time, highest_temp)
        rows.append(csv_data)

        # incriment the sensors by 1
        sensor_id += 1


# this function is the pipe_activitys journey through the pipe
def sensor_generator(env, start_temperature, highest_temp, start_vibration, limit_temperature, limit_vibration, single_sensor_runtime, sensor, warning_temp, warning_vib):
    
    # record the time the pipe_activity starts changing tempreture at this sensor
    current_time = f'{env.now:5.2f}'

    # temperature
    temperature = start_temperature
    vibration = start_vibration

    files.get_sensor_id()
    # temperture alert conditions
    temp_warning = False
    temp_alerm = False
    temp_emergency = False

    # vibration alert conditions
    vib_warning = False
    vib_alerm = False
    vib_emergency = False
   # catch vibration alerts: [warning, alerm, emergency]
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
    
    # get the staring states of each sensor
    rows.append([files.get_sensor_id(),current_time,start_temperature,start_vibration])
    alarm_rows.append([files.get_sensor_id(),current_time, temp_warning,vib_warning, temp_alerm,vib_alerm,temp_emergency,vib_emergency])

    # request the sensor data
    with sensor.request() as req:

        con_time = random.expovariate(1.0 / single_sensor_runtime)

        while True:
            # reset values to false
            # temperture alert conditions
            temp_warning = False
            temp_alerm = False
            temp_emergency = False

            # vibration alert conditions
            vib_warning = False
            vib_alerm = False
            vib_emergency = False

            # ensure the new id remains constant
            files.get_sensor_id()

            # random number generator
            interarrival = random.expovariate(files.get_sensor_id() + 1)
            # simulate vibration spikes
            vibration = secrets.randbelow(start_vibration)

            # ensure the vibration is always above 0
            while vibration == 0:
                vibration = secrets.randbelow(start_vibration)

            # limit temperture from running away
            if temperature > limit_temperature:
                print("pipe temperture limit reached")
                temperature -= random.expovariate(1.0 /
                                                  interarrival) + (highest_temp / 3)
            else:
                temperature += random.expovariate(1.0/interarrival)

            # catch vibration alerts: [warning, alerm, emergency]
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
            time = f'{env.now + 0.01:5.2f}'
            temperature_current = f'{temperature:5.2f} '
            vibration_current = f'{vibration}'
            
            # fields = ['sensor_number', 'time','temperature','vibration']
            # alarm_feilds = ['sensor_number', 'time','temp_alert','vib_alarm','temp_warning','vib_warning','temp_emergency','vib_emergency']
            print(f'{files.get_sensor_id()} {time}  {temperature_current} {vibration_current}')
            rows.append([files.get_sensor_id(),time,temperature_current,vibration_current])
            # rows.append(current_viv_values)
            alarm_rows.append([files.get_sensor_id(),time, temp_warning,vib_warning, temp_alerm,vib_alerm,temp_emergency,vib_emergency])
            # instead of yielding the arrival time, yield a Timeout Event
            yield env.timeout(interarrival, highest_temp)


# initlise the descrete event simulation enviroment
env = simpy.Environment()
sensor = simpy.Resource(env, capacity=1)

# starting tempreture & vibration
start_temperature = int(files.get_start_temperature())
start_vibration = int(files.get_start_vibration())

# pipe limit for tempreture and vibration
limit_temperature = int(files.get_limit_temperature())
limit_vibration = int(files.get_limit_vibration())

# max time each sensor can run. will be timed by three for the number of sensors
single_sensor_runtime = int(files.get_test_time())

# [warning, alerm, emergency]
warning_temp = [files.get_sensor_temp_warning(
), files.get_sensor_temp_alart(), files.get_sensor_temp_emergency()]
warning_vib = [files.get_sensor_vib_warning(
), files.get_sensor_vib_alart(), files.get_sensor_vib_emergency()]

env.process(pipe_generator(env, start_temperature, start_vibration, limit_temperature,
            limit_vibration, single_sensor_runtime, sensor, warning_temp, warning_vib, rows))

sensor_number = int(files.get_sensor())
# run the simulation. calculated by: number of sensors (3) and how long they can each run for (single_sensor_runtime) 
env.run(until=single_sensor_runtime * sensor_number)


# writing to csv file
with open(filename, 'w') as csvfile:
    # creating a csv writer object
    csvwriter = csv.writer(csvfile)
    # writing the fields
    csvwriter.writerow(fields)
    # writing the data rows
    csvwriter.writerows(rows)

# write csv for alarms 
with open(alarm_file,'w') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(alarm_feilds)
    csvwriter.writerows(alarm_rows)

# clean the csv by removing empty rows
files.clean_csv(filename)
files.clean_csv(alarm_file)