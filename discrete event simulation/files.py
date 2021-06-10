import pandas as pd
import csv
sensor_id = []
#create text file to store value 
def create_text(name, value):
    with open(f'{name}.txt', 'w') as f:
        f.write(f'{value}')

# get value from text file
def get_text_value(txt_name):
    value = float(open(f"{txt_name}.txt", "r").read())
    return value

# clean csv from empty rows
def clean_csv(name):
    # read the csv file
    df = pd.read_csv(f'{name}')
    # remove all empty rows where index is false 
    df.to_csv(f'{name}', index=False)

# get the config file
with open("discrete event simulation\Configuration_Data.csv") as file_name:
    file_read = csv.reader(file_name)
    #  get the array and remove the first row
    array = list(file_read)

#  set getters for each config element: gets values from specific indexes of a csv file turned into an array
def get_start_temperature():
    return float(array[0])

def get_limit_temperature():
    return float(array[1])

def get_start_vibration():
    return float(array[2])

def get_limit_vibration():
    return float(array[3])

def get_test_time():
    return float(array[4])

def get_sensor_temp_warning():
    return float(array[5])

def get_sensor_temp_alart():
    return float(array[6])

def get_sensor_temp_emergency():
    return float(array[7])

def get_sensor_vib_warning():
    return float(array[8])

def get_sensor_vib_alart():
    return float(array[9])

def get_sensor_vib_emergency():
    return float(array[10])

def get_sensor():
    return float(array[11])

def set_sensor_id(current_id):
    sensor_id.append(current_id)
    return current_id

def get_sensor_id():
    return sensor_id[-1]
