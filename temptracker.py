import time, glob, csv, argparse, os, pyowm

def getRawData():
    # Dump the output of the device file
    device_file = glob.glob('/sys/bus/w1/devices/28*')[0] + '/w1_slave'
    with open(device_file, 'r') as raw_data:
        lines = raw_data.readlines()
        return lines

def getTemp(offset):
    raw_data = getRawData()
    # Make sure the data is read successfully
    while raw_data[0].strip()[-3:] != 'YES':
        time.sleep(0.5)
        raw_data = getRawData()
    # Find the entry for temperature and make sure the decimal is in
    # the correct position
    read_pos = raw_data[1].find('t=')
    if read_pos != -1:
        temp_string = raw_data[1][read_pos+2:]
        return (float(temp_string) / 1000.0) + offset
    
def getExternalTemp(owm_api, location):
    # Connect to OpenWeatherMap to find outdoors temperature
    owm = pyowm.OWM(owm_api)
    location = owm.weather_at_place(location)
    weather = location.get_weather()
    return weather.get_temperature('celsius')['temp']

def main(filepath, offset, owm_api, location):
    # Try to record data, skip this attempt if an error is encountered
    try:
        # Get the timestamp and read sensor data
        if not owm_api and not location:
            fieldnames = ['timestamp', 'temperature']
            data_dict = {'timestamp': time.strftime('%c', time.localtime()),
                         'temperature': getTemp(offset)}
        else:
            fieldnames = ['timestamp', 'temperature', 'external_temperature']
            data_dict = {'timestamp': time.strftime('%c', time.localtime()),
                         'temperature': getTemp(offset), 
                         'external_temperature': getExternalTemp(owm_api, location)}
    except:
        err = sys.exc_info()[0]
        print("TempTracker: {}".format(err), file=sys.stderr)
        print("TempTracker encountered an error and skipped a scheduled measurement", file=sys.stderr)
        sys.exit(1)

    # if the file dosen't already exist exists create it and write
    # header + initial data
    if not os.path.isfile(filepath):
        with open(filepath, 'w+', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerow(data_dict)
    # if it does exist then append new data onto existing time series
    else:
        with open(filepath, 'a', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writerow(data_dict)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    default_path = os.path.expanduser('~') + '/temp_history.csv'
    parser.add_argument('-p', '--path', dest='pathname', type=str, required=False, 
            help='the full path for the output file', default=default_path)
    parser.add_argument('-o', '--offset', dest='offset', type=float, required=False,
            help='the offset for the temperature sensor in celsius (defaults to 0)',       
            default=0)
    parser.add_argument('-k', '--owm', dest='owm_api', type=str, required=False,
                       help='OpenWeatherMap api key for external temperature data', default='')
    parser.add_argument('-l', '--location', dest='location', type=str, required=False,
                       help='OpenWeatherMap location for external temperature data', default='')
    args = parser.parse_args()
    main(args.pathname, args.offset, args.owm_api, args.location)
