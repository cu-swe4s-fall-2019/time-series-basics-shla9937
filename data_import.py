import csv
import dateutil.parser
import os
from os import listdir
from os.path import isfile, join
import argparse
import datetime


class ImportData:
    def __init__(self, data_csv, resolution):
        self._time = []
        self._value = []
        self._roundtime = []
        self._roundtimeStr = []
        with open(data_csv, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                try:
                    self._time.append(dateutil.parser.parse(row['time']))
                except ValueError:
                    print('Bad input format for time')
                    print(row['time'])
                if row['value'] == 'low':
                    self._value.append(40)
                    print('Replacing '+str(row['value']+' with 40.'))
                elif row['value'] == 'high':
                    self._value.append(300)
                    print('Replacing '+str(row['value']+' with 300.'))
                elif row['value'] is None:
                    self._time.pop()
                    continue
                else:
                    self._value.append(row['value'])
        for item in self.roundTimeArray(resolution):
            data_time.append(item)
        for item in self._value:
            data_value.append(item)

    def linear_search_value(self, key_time):
        for i in range(len(self._roundtimeStr)):
            curr = self._roundtimeStr[i]
            if key_time == curr:
                return self._value[i]
        return -1

    def roundTimeArray(self, resolution):
        for times in self._time:
            minminus = datetime.timedelta(minutes=(times.minute % resolution))
            minplus = datetime.timedelta(minutes=resolution) - minminus
            if (times.minute % resolution) <= resolution/2:
                newtime = times - minminus
            else:
                newtime = times + minplus
            self._roundtime.append(newtime)
            self._roundtimeStr.append(newtime.strftime("%m/%d/%Y %H:%M"))
        return self._roundtimeStr


def printArray(data_list, annotation_list, base_name, key_file):
    base_data = []
    key_idx = 0
    for i in range(len(annotation_list)):
        if annotation_list[i] == key_file:
            base_data = zip(data_list[i]._roundtimeStr, data_list[i]._value)
            print('base data is: '+annotation_list[i])
            key_idx = i
            break
        if i == len(annotation_list):
            print('Key not found')

    file = open(base_name+'.csv', 'w')
    file.write('time,')

    file.write(annotation_list[key_idx][0:-4]+', ')

    non_key = list(range(len(annotation_list)))
    non_key.remove(key_idx)

    for idx in non_key:
        file.write(annotation_list[idx][0:-4]+', ')
    file.write('\n')

    for time, value in base_data:
        file.write(time+', '+value+', ')
        for n in non_key:
            if time in data_list[n]._roundtimeStr:
                file.write(str(data_list[n].linear_search_value(time))+', ')
            else:
                file.write('0, ')
        file.write('\n')
    file.close()


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='A class to import' +
                                     'combine, and print data from a folder.',
                                     prog='dataImport')

    parser.add_argument('--folder_name', type=str, help='Name of the folder')

    parser.add_argument('--output_file', type=str, help='Name of Output file',
                        required=False)

    parser.add_argument('--sort_key', type=str, help='File to sort on',
                        required=False)

    parser.add_argument('--number_of_files', type=int,
                        help="Number of Files", required=False)

    args = parser.parse_args()

    data_list = []
    num_files = 0
    Path = args.folder_name
    filelist = os.listdir(Path)
    for x in filelist:
        if x.endswith('.csv'):
            try:
                with open(Path + x, 'r') as f:
                    data_list.append(Path + x)
                    num_files += 1
            except BaseException:
                print(x+' is not .csv file.')

    data_5 = []
    data_15 = []
    data_time = []
    data_value = []

    for data_csv in data_list:
        ImportData(data_csv, 5)
        data_5.append(list(zip(data_time, data_value)))
        data_time = []
        data_value = []

    for data_csv in data_list:
        ImportData(data_csv, 15)
        data_15.append(list(zip(data_time, data_value)))
        data_time = []
        data_value = []

    print(list(data_15))
