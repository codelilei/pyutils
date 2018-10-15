# coding: utf-8

'''
extract and calculate average time from log file.
log format sample:
    com.example.androidtest I/test: [200]
    com.example.androidtest D/Android: Module1 time: 5.194052
    Module2 time: 5.744004
    com.example.androidtest D/Android: Module3 time: 5.188264
    com.example.androidtest D/Android: Module4 time: 4.188000
    I/System.out: Module5 time: 6.168247
        AVG_TIME：34ms
    com.example.androidtest D/CAndroid: Module6 time: 3.846000
    repeat more...
'''

import os
import sys
import re
import csv
import codecs
import numpy as np


def extract_time(log_file, time_thresh=0.1):
    """
    Args:
        log_file: path of log file
        time_thresh: filter time less than time_thresh
    """
    if not os.path.isfile(log_file):
        print('file not found')
        sys.exit()

    module_names = [
        'SampleModule1', 'SampleModule2',
        'SampleModule3', 'SampleModule4',
        'SampleModule5', 'SampleModule6'
    ]

    regs = [re.compile(module + ' time: (\d+\.\d+)')
            for module in module_names]

    data = {}

    with codecs.open(log_file, 'r', 'utf-8') as fd:
        # rd = csv.reader(fd)
        for line in fd:
            line = line.strip()
            if not line:
                continue

            # if line.startswith('###'):
            for reg, module in zip(regs, module_names):
                reg_match = reg.search(line)
                if reg_match:
                    t = float(reg_match.group(1))
                    # dv = data.get(module)
                    # if dv is None:
                    #      data[module] = [t]
                    # else:
                    #     data[module].append(t)
                    try:
                        data[module].append(t)
                    except:
                        data[module] = [t]
                    break

    # print(data)
    print('======Time Summary======')
    for k, v in data.items():
        t_arr = np.array(v)
        print(k + ' AvgTime: %.2f' % np.mean(t_arr[t_arr > time_thresh]))

    # save result to csv
    with open('extract-time.csv', 'w') as fd:
        # write header
        # writer = csv.DictWriter(fd, fieldnames=fieldnames)
        # writer.writeheader()
        # for kv in data.values():
        #     writer.writerow(kv)

        writer = csv.writer(fd)
        writer.writerow(module_names)
        for k, v in data.items():
            writer.writerow(v)


if __name__ == '__main__':
    extract_time('time.log')
