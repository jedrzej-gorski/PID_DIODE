from bokeh.plotting import figure, output_file, save
import numexpr

class PID:
    def __init__(self, diode_data, env_data, res_data, simulation_time, setpoint):
        self.environment_formula = env_data
        self.simulation_time = simulation_time
        self.interval_time = simulation_time / 1000
        self.error = [0]
        self.setpoint_intensity = setpoint
        self.environment_intensity = [self.calculate_new_environment(0.0, self.environment_formula)]
        self.input_intensity = [self.environment_intensity[0]]
        self.output_intensity = []
        self.intensity_coefficient = diode_data[0]
        self.intensity_offset = diode_data[3]
        self.signal = []
        self.voltage = []
        self.timestamp = [0.0]
        self.voltage_drop = diode_data[4] * res_data
        self.max_voltage = diode_data[2] + self.voltage_drop
        self.min_voltage = diode_data[1] + self.voltage_drop

    def calculate_error(self, setpoint, input):
        return setpoint - input

    def calculate_signal(self, error):
        proportional_coefficient = 0.02085
        integration_time = 0.002
        derivative_time = 0.000667
        error_difference = error[-1] - error[-2]
        new_signal = proportional_coefficient * (error[-1] + self.interval_time / integration_time * sum(error) +
                                                 derivative_time * error_difference / self.interval_time)
        return max(0, min(new_signal, 20))

    def calculate_voltage(self, new_signal):
        new_voltage = (self.max_voltage - self.min_voltage) * 1 / 20 * new_signal + self.min_voltage
        return new_voltage

    def calculate_output_intensity(self, new_voltage):
        new_output = (new_voltage - self.voltage_drop) * self.intensity_coefficient + self.intensity_offset
        return new_output

    def calculate_new_input(self, new_environment, new_output):
        new_input = new_environment + new_output
        return new_input

    def calculate_new_environment(self, time, env_data):
        x = time
        return float(numexpr.evaluate(env_data))

    def run_pid(self):
        for i in range(int(self.simulation_time / self.interval_time)):
            self.timestamp.append((i + 1) * self.interval_time)
            self.error.append(self.calculate_error(self.setpoint_intensity, self.input_intensity[-1]))
            self.signal.append(self.calculate_signal(self.error))
            self.voltage.append(self.calculate_voltage(self.signal[-1]))
            self.output_intensity.append(self.calculate_output_intensity(self.voltage[-1]))
            self.environment_intensity.append(
                self.calculate_new_environment(self.timestamp[-1],
                                               self.environment_formula))
            self.input_intensity.append(
                self.calculate_new_input(self.environment_intensity[-1], self.output_intensity[-1]))
        print("--------------------------------------")
        print(self.input_intensity[0:50])
        print(self.output_intensity[0:50])
        print(self.voltage[0:50])
        print(self.signal[0:50])
        print(self.error[0:50])
        output_file(filename="linia.html", title="Wykres natężenia oświetlenia")
        p = figure(title="Wykres natężenia oświetlenia", x_axis_label="Czas (s)", y_axis_label="Nateżenie oświetlenia (lx)")
        p.line(self.timestamp, self.input_intensity, line_width=2, line_color="#037EF3")
        save(p)
        output_file(filename="linia1.html", title="Wykres natężenia diody")
        r = figure(title="Wykres natężenia diody", x_axis_label="Czas (s)", y_axis_label="Nateżenie oświetlenia (lx)")
        r.line(self.timestamp[0:1000], self.output_intensity, line_width=2, line_color="#F85A40")
        save(r)
        output_file(filename="linia2.html", title="Wykres natężenia środowiska")
        q = figure(title="Wykres natężenia środowiska", x_axis_label="Czas (s)", y_axis_label="Nateżenie oświetlenia (lx)")
        q.line(self.timestamp, self.environment_intensity, line_width=2, line_color="#00C16E")
        save(q)
        output_file(filename="linia3.html", title="Wykresy natężenia oświetlenia")
        s = figure(title="Wykresy natężenia oświetlenia", x_axis_label="Czas (s)", y_axis_label="Natężenie oświetlenia (lx)")
        s.line(self.timestamp, self.input_intensity, line_width=2, line_color="#037EF3", legend_label="Natężenie całkowite")
        s.line(self.timestamp[0:1000], self.output_intensity, line_width=2, line_color="#F85A40", legend_label="Natężenie diody")
        s.line(self.timestamp, self.environment_intensity, line_width=2, line_color="#00C16E", legend_label="Natężenie środowiska")
        save(s)
