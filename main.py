from bokeh.plotting import figure, output_file, show

output_file("line.html")

simulationTime = 1                        # wyrażone w sekundach
intervalTime = 0.001
error = [0]
setpointIntensity = 340                     # wyrażone w luxach
environmentCoefficient = -250
environmentIntensity = [300]                # dla przykładu stała. Ienv(0) = 300
inputIntensity = [environmentIntensity[0]]  # Iin(1) = Ienv(0) + Iout(0)
outputIntensity = []                        # Iout(0) = 0, bo dioda jest wyłączona
intensityCoefficient = 2.89 * 10 ** 2       # współczynnik zależności liniowej między napięciem, a natężeniem oświetlenia
intensityOffset = -722.5
signal = []
voltage = []
timestamp = [0]

def calculateError(setpoint, input):
    return setpoint - input

def calculateSignal(error):
    proportionalCoefficient = 0.02085
    integrationTime = 0.001
    derivativeTime = 0.000667
    errorDifference = error[-1] - error[-2]
    newSignal = proportionalCoefficient * (error[-1] + intervalTime / integrationTime * sum(error) + derivativeTime * errorDifference / intervalTime)
    return max(0, min(newSignal, 20))

def calculateVoltage(newSignal):
    newVoltage = 1/20 * newSignal + 3
    return newVoltage

def calculateOutputIntensity(newVoltage):
    newOutput = (newVoltage - 0.5) * intensityCoefficient + intensityOffset
    return newOutput

def calculateNewInput(newEnvironment, newOutput):
    newInput = newEnvironment + newOutput
    return newInput

def calculateNewEnvironment(environmentCoefficient, time, environmentOffset):
    newEnvironment = environmentCoefficient * time + environmentOffset
    return newEnvironment

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    for i in range(int(simulationTime / intervalTime)):
        timestamp.append((i + 1) * intervalTime)
        error.append(calculateError(setpointIntensity, inputIntensity[-1]))
        signal.append(calculateSignal(error))
        voltage.append(calculateVoltage(signal[-1]))
        outputIntensity.append(calculateOutputIntensity(voltage[-1]))
        environmentIntensity.append(calculateNewEnvironment(environmentCoefficient, timestamp[-1], environmentIntensity[0]))
        inputIntensity.append(calculateNewInput(environmentIntensity[-1], outputIntensity[-1]))

print(inputIntensity[0:50])
print(outputIntensity[0:50])
print(voltage[0:50])
print(signal[0:50])
print(error[0:50])

p = figure()
r = figure()
p.line(timestamp, inputIntensity, line_width=2)
r.line(timestamp[0:1000], outputIntensity, line_width=2)
show(p)
show(r)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
