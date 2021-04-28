# differnt levels of alert
# these two elements are instances of each sensor
tempretureSensor = {
    "testId": 1,
    "testTime": "12/2/2021",
    #alert level using array five levels of alert from. safe, good, 
    "tempLimit": [1,2,3,4,5],
    # not sensor 
    "numberOfTest": 3,
}
vibrationSensor = {
    # will be randomly assigned
    "id": 1,
    # [0]Safe [1]Good [2]Warning [3]Extreme Warning [4]Danger
    "alert": [],
    "testTime": "12/2/2021"
}

testTime = int(input("Enter a test time: "))
print(f"Test time: {testTime}")
sensorRequirement["testTime"] = testTime

tempLimit = float(input("Enter a tempreture limit: "))
print(f"Tempreture limit: {tempLimit}")
sensorRequirement["tempLimit"] = tempLimit

vibLimit = float(input("Enter a vibration limit: "))
print(f"vibation limit: {vibLimit}")
sensorRequirement["vibLimit"] = vibLimit

numberOfTest = int(input("Enter how many tests to run: "))
print(f"running {numberOfTest} tests")
sensorRequirement["numberOfTest"] = numberOfTest

print(sensorRequirement)
