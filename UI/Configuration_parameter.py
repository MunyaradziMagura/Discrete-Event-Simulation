class Configuration_parameter:
    def __init__(self):  # Constructor
        self.start_temperature = 0
        self.start_vibration = 0
        self.limit_temperature = 0
        self.limit_vibration = 0
        self.sensor_interval_time = 0
        self.senor_temp_warning = 0
        self.senor_temp_alarm = 0
        self.senor_temp_emergency = 0
        self.senor_vib_warning = 0
        self.senor_vib_alarm = 0
        self.senor_vib_emergency = 0

    def get_start_temperature(self):
        return self.start_temperature

    def set_start_temperature(self, value):
        self.start_temperature = value

    def get_start_vibration(self):
        return self.start_vibration

    def set_start_vibration(self, value):
        self.start_vibration = value

    def get_limit_temperature(self):
        return self.limit_temperature

    def set_limit_temperature(self, value):
        self.limit_temperature = value

    def get_limit_vibration(self):
        return self.limit_temperature

    def set_limit_vibration(self, value):
        self.limit_vibration = value

    def get_sensor_interval_time(self):
        return self.sensor_interval_time

    def set_sensor_interval_time(self, value):
        self.sensor_interval_time = value

    def get_temp_sensor_warning(self):
        return self.senor_temp_warning

    def set_temp_sensor_warning(self, value):
        self.senor_vib_warning = value

    def get_vib_sensor_warning(self):
        return self.senor_vib_warning

    def set_vib_sensor_warning(self, value):
        self.senor_vib_warning = value

    def get_temp_sensor_alarm(self):
        return self.senor_temp_alarm

    def set_temp_sensor_alarm(self, value):
        self.senor_temp_alarm = value

    def get_vib_sensor_alarm(self):
        return self.senor_vib_alarm

    def set_vib_sensor_alarm(self, value):
        self.senor_vib_alarm = value

    def get_temp_sensor_emergency(self):
        return self.senor_temp_emergency

    def set_temp_sensor_emergency(self, value):
        self.senor_temp_emergency = value

    def get_vib_sensor_emergency(self):
        return self.senor_vib_emergency

    def set_vib_sensor_emergency(self, value):
        self.senor_vib_emergency = value
