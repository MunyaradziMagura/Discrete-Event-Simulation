import csv 
import constants
print(constants.id)


# field names 
fields = ['time','sensor_one_temp','sensor_one_warning','sensor_one_alarm','sensor_one_emergency',
            'sensor_two_temp','sensor_two_warning','sensor_two_alarm','sensor_two_emergency',
            'sensor_three_temp','sensor_three_warning','sensor_three_alarm','sensor_three_emergency'
            
            ,'sensor_one_vib','sensor_one_warning_vib','sensor_one_alarm_vib','sensor_one_emergency_vib',
            'sensor_two_temp_vib','sensor_two_warning_vib','sensor_two_alarm_vib','sensor_two_emergency_vib'
            'sensor_three_temp_vib','sensor_three_warning_vib','sensor_three_alarm_vib','sensor_three_emergency_vib']
# data rows of csv file 
rows = [ ['Nikhil', 'COE', '2', '9.0'], 
         ['Sanchit', 'COE', '2', '9.1'], 
         ['Aditya', 'IT', '2', '9.3'], 
         ['Sagar', 'SE', '1', '9.5'], 
         ['Prateek', 'MCE', '3', '7.8'], 
         ['Sahil', 'EP', '2', '9.1']] 
    
# name of csv file 
filename = "university_records.csv"
    
# writing to csv file 
with open(filename, 'w') as csvfile: 
    # creating a csv writer object 
    csvwriter = csv.writer(csvfile) 
        
    # writing the fields 
    csvwriter.writerow(fields) 
        
    # writing the data rows 
    csvwriter.writerows(rows)