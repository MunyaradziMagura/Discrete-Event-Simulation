import simpy
import random
import secrets
import csv 

# stores all the file functions 
import files

# field names for csv
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

# write the id to an external text file for storage and dataloss prevention
def identification(id):
    
    #add sensor data
    with open('id.txt', 'w') as f:
        f.write(f"{id}\n")
    return id


#  generate the pipe 
def pipe_generator(env, start_temperature, start_vibration, limit_temperature, limit_vibration, sensor_interval_time, sensor, warning_temp,warning_vib,rows):
    
    # inilise which sensor is being simulated & what is the highest temp
    sensor_id = 0
    highest_temp = 0
    
    # print for clearity when looking at terminal output 
    print("sensor1  | sensor2 | sensor3")

    # because there are only three sensors
    while True and sensor_id < 3:
       
        # set id
        identification(sensor_id)
        
        # store csv data into this array for each sensor 
        csv_data = []
       
        # add the last temp to the new 
        if highest_temp > 0:
            
            # update stating temp
            start_temperature += highest_temp - start_temperature
        
        #  create an instance of the water within the pipe
        water = sensor_generator(env, sensor_id,start_temperature,highest_temp, start_vibration, limit_temperature, limit_vibration, sensor_interval_time, sensor, warning_temp,warning_vib)

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

    # temperature 
    temperature = start_temperature
    vibration = start_vibration
   
    new_id = int(open("id.txt", "r").read())
    # temperture alert conditions
    temp_warning = False
    temp_alerm = False
    temp_emergency = False

    # vibration alert conditions
    vib_warning = False
    vib_alerm = False
    vib_emergency = False

    # get the staring states of each sensor
    if new_id == 0:
        
        # set sensor one data
        sensor_one_data = [f'{temperature:5.2f} ',f'{vib_warning}',f'{temp_alerm}',f'{temp_emergency}',f'{vibration}',f'{vib_warning}',f'{vib_alerm}',f'{vib_emergency}']
        sensor_two_data = [f'{start_temperature}','','','',f'{start_vibration}','','','']
        sensor_three_data = [f'{start_temperature}','','','',f'{start_vibration}','','','']
        
        #append the data to the csv rows array
        rows.append([f'{current_time:5.3f}'] + sensor_one_data + sensor_two_data + sensor_three_data)
        
    # request the sensor data
    with sensor.request() as req:
        
        con_time = random.expovariate(1.0 / sensor_interval_time)
        
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
            print(f"current_time {env.now:5.2f} |" ,end="")
            time = [f'{env.now + 0.01:5.2f}']
            if new_id == 0:
               
                # print data to terminal
                print( f' temp changed to {temperature:5.2f} degree/s Celsius at {env.now:5.2f} min/s || vibrated by {vibration} cubic meters |', end="")
                print("N/A   |", end="")  # sensor id = 1
                print("N/A")  # sensor id = 2
                
                # time, warnings
                # set sensor one data
                sensor_one_data = [f'{temperature:5.2f} ',f'{vib_warning}',f'{temp_alerm}',f'{temp_emergency}',f'{vibration}',f'{vib_warning}',f'{vib_alerm}',f'{vib_emergency}']
                sensor_two_data = [f'{start_temperature}','','','',f'{start_vibration}','','','']
                sensor_three_data = [f'{start_temperature}','','','',f'{start_vibration}','','','']
                
                #append the data to the csv rows array
                rows.append(time + sensor_one_data + sensor_two_data + sensor_three_data)
                
                # write last tempreture to an exturnal text file
                temp_sen_0 = files.create_text('temp0', f'{temperature:5.2f}')
                
                #store last vibration value
                vib_sen_0 = files.create_text('vib0', f'{vibration:5.2f}')
                
            elif new_id == 1:
                print("N/A   |", end="")  # sensor id = 0
                print( f' temp changed to {temperature:5.2f} degree/s Celsius at {env.now:5.2f} min/s || vibrated by {vibration} cubic meters |', end="")
                print("N/A   |")  # sensor id = 2
                
                #get previous sensors last values both temperture and vibration
                last_temp_senor_0 = files.get_text_value("temp0")
                last_vib_senor_0 = files.get_text_value("vib0")

                # create arrays to store the values
                sensor_one_data = [f'{last_temp_senor_0}','','','',f'{last_vib_senor_0}','','','']
                sensor_two_data = [f'{temperature:5.2f} ',f'{vib_warning}',f'{temp_alerm}',f'{temp_emergency}',f'{vibration}',f'{vib_warning}',f'{vib_alerm}',f'{vib_emergency}']
                sensor_three_data = [f'{start_temperature}','','','',f'{start_vibration}','','','']
                rows.append(time + sensor_one_data + sensor_two_data + sensor_three_data)
                
                #save last temp values to text files
                temp_sen_1 = files.create_text('temp1',  f'{temperature:5.2f}')
                vib_sen_1 = files.create_text('vib1', f'{vibration:5.2f}')


            elif new_id == 2:
                print("N/A   |", end="")  # sensor id = 0
                print("N/A   |", end="")  # sensor id = 1
                print( f' temp changed to {temperature:5.2f} degree/s Celsius at {env.now:5.2f} min/s || vibrated by {vibration} cubic meters |')  
                
                last_temp_senor_0 = files.get_text_value("temp0")
                last_vib_senor_0 = files.get_text_value("vib0")
                last_temp_senor_1 = files.get_text_value("temp1")
                last_vib_senor_1 = files.get_text_value("vib1")

                sensor_one_data = [f'{last_temp_senor_0}','','','',f'{last_vib_senor_0}','','','']
                sensor_two_data = [f'{last_temp_senor_1}','','','',f'{last_vib_senor_1}','','','']
                sensor_three_data = [f'{temperature:5.2f} ',f'{vib_warning}',f'{temp_alerm}',f'{temp_emergency}',f'{vibration}',f'{vib_warning}',f'{vib_alerm}',f'{vib_emergency}']
                rows.append(time + sensor_one_data + sensor_two_data + sensor_three_data)
                temp_sen_2 = files.create_text('temp2',  f'{temperature:5.2f}')
                vib_sen_2 = files.create_text('vib2', f'{vibration:5.2f}')

            # instead of yielding the arrival time, yield a Timeout Event
            yield env.timeout(interarrival,highest_temp)

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
sensor_interval_time = int(files.get_test_time())

# [warning, alerm, emergency]
warning_temp = [files.get_sensor_temp_warning(), files.get_sensor_temp_alart(), files.get_sensor_temp_emergency()]
warning_vib = [files.get_sensor_vib_warning(), files.get_sensor_vib_alart(), files.get_sensor_vib_emergency()]

env.process(pipe_generator(env, start_temperature, start_vibration, limit_temperature, limit_vibration, sensor_interval_time, sensor, warning_temp,warning_vib,rows))

# run the simulation. calculated by: number of sensors (3) and how long they can each run for (sensor_interval_time)
env.run(until=sensor_interval_time * 3)


# writing to csv file 
with open(filename, 'w') as csvfile: 
    # creating a csv writer object 
    csvwriter = csv.writer(csvfile) 
    # writing the fields 
    csvwriter.writerow(fields) 
    # writing the data rows 
    csvwriter.writerows(rows)

# clean the csv by removing empty rows
files.clean_csv(filename)