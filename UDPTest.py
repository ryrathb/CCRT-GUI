
speed_difference_dict = {'10': [], '20': [], '30': [], '40': [], '50': [], '60': []}

def find_init_torque_time(commandedRPM, tempArray, sampleRate):
    init_torque_time = []
    for i in range(0, len(tempArray)):
        for j in range(0, len(tempArray[i])):
            if tempArray[i][j] < (commandedRPM - 1):
                init_torque_time.append(j * sampleRate)
                break
        
    return init_torque_time 

def find_time_to_stop(tempArray, sampleRate):
    time_to_stop = []
    for i in range(0, tempArray):
        for j in range(0, tempArray[i]):
            if tempArray[i][j] < 0.5:
                time_to_stop.append(j * sampleRate)

    return time_to_stop 

def find_peak_torque(tempArray, speed_difference_dict, sampleRate, commandedRPM):
    peak_torque = [0, 0]

    for i in range(0, tempArray):
        for j in range(0, tempArray[i]):
            observed_difference = tempArray[i][j+1] - tempArray[i][j]
            if abs(observed_difference - speed_difference_dict[commandedRPM][j]) > peak_torque[i]:
                peak_torque[i] = j * sampleRate 

    return peak_torque
        