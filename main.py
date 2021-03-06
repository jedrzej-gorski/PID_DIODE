from bokeh.plotting import figure, output_file, show
import gui

#output_file("line.html")


class PID:
    def __init__(self):
        self.simulation_time = 1
        self.interval_time = 0.001
        self.error = [0]
        self.setpoint_intensity = 340
        self.environment_coefficient = -250
        self.environment_intensity = [300]
        self.input_intensity = [self.environment_intensity[0]]
        self.output_intensity = []
        self.intensity_coefficient = 2.89 * 10 ** 2
        self.intensity_offset = -722.5
        self.signal = []
        self.voltage = []
        self.timestamp = [0.0]

    def calculate_error(self, setpoint, input):
        return setpoint - input

    def calculate_signal(self, error):
        proportional_coefficient = 0.02085
        integration_time = 0.001
        derivative_time = 0.000667
        error_difference = error[-1] - error[-2]
        new_signal = proportional_coefficient * (error[-1] + self.interval_time / integration_time * sum(error) +
                                                 derivative_time * error_difference / self.interval_time)
        return max(0, min(new_signal, 20))

    def calculate_voltage(self, new_signal):
        new_voltage = 1 / 20 * new_signal + 3
        return new_voltage

    def calculate_output_intensity(self, new_voltage):
        new_output = (new_voltage - 0.5) * self.intensity_coefficient + self.intensity_offset
        return new_output

    def calculate_new_input(self, new_environment, new_output):
        new_input = new_environment + new_output
        return new_input

    def calculate_new_environment(self, environment_coefficient, time, environment_offset):
        new_environment = environment_coefficient * time + environment_offset
        return new_environment

    def run_pid(self):
        for i in range(int(self.simulation_time / self.interval_time)):
            self.timestamp.append((i + 1) * self.interval_time)
            self.error.append(self.calculate_error(self.setpoint_intensity, self.input_intensity[-1]))
            self.signal.append(self.calculate_signal(self.error))
            self.voltage.append(self.calculate_voltage(self.signal[-1]))
            self.output_intensity.append(self.calculate_output_intensity(self.voltage[-1]))
            self.environment_intensity.append(
                self.calculate_new_environment(self.environment_coefficient, self.timestamp[-1],
                                               self.environment_intensity[0]))
            self.input_intensity.append(
                self.calculate_new_input(self.environment_intensity[-1], self.output_intensity[-1]))
        print(self.input_intensity[0:50])
        print(self.output_intensity[0:50])
        print(self.voltage[0:50])
        print(self.signal[0:50])
        print(self.error[0:50])





# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    pid_algorithm = PID()
    pid_algorithm.run_pid()
    application = gui.GUIApp()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
