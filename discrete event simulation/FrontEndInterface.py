#


class FrontEndInterface:
    def __init__(self):
        self.start_temperature = None
        self.start_vibration = None
        self.limit_temperature = None
        self.limit_vibration = None
        self.sensor_interval_time = None

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
