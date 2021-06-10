import csv 
csv_dictionary = {}
csv_length = 0
with open('sensor_data.csv', 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        csv_length += 1
        # print(row[1])
        time = row[1]
        temp = row[2]
        vib = row[3]
        if str(row[0]) in csv_dictionary:
            # add time
            csv_dictionary[str(row[0])][0].append(time) 
            # add temp
            csv_dictionary[str(row[0])][1].append(temp)
            # add vib
            csv_dictionary[str(row[0])][2].append(vib)
        else:
            csv_dictionary[str(row[0])] = [[time],[temp],[vib]]
    csv_dictionary.pop("sensorID")

print(csv_dictionary[str()][1])
