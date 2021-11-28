#!/usr/bin/env python3

# read the ice7g ice model from Peltier and construct ice input file for taboo.

import os
import netCDF4 as nc


def readi7g(i7g_path):
    time = list()
    all_data = list()

    i7g_path = str(i7g_path)
    i7g_relative_files = [file for file in os.listdir(i7g_path) if not os.path.isdir(os.path.join(i7g_path, file))]
    i7g_files = [os.path.join(i7g_path, file) for file in i7g_relative_files]

    DATA = nc.Dataset(i7g_files[0])
    lon = list(DATA.variables['lon'][:])
    lat = list(DATA.variables['lat'][:])
    shape = tuple(DATA.variables['stgit'].shape)

    for i7g_file in i7g_files:
        DATA = nc.Dataset(i7g_file)
        time.append(DATA.variables['stgit'].input_time)
    time.sort()
    print(time)

    for loni in range(0, shape[1]):
        print(str(lon[loni]))
        for lati in range(0, shape[0]):
            # print(str(lon[loni]) + ' ' + str(lat[lati]))
            data = dict()
            data['lon'] = float(lon[loni])
            data['lat'] = float(lat[lati])
            data['thick'] = []

            for i7g_file in i7g_files:
                DATA = nc.Dataset(i7g_file)
                data['thick'].append(DATA['stgit'][lati][loni])

            all_data.append(data)
            del data
    # print(all_data)

    d0_data = list()
    all0_data = list()
    for item in all_data:
        if any(item['thick']):
            d0_data.append(item)
        else:
            all0_data.append(item)

    with open('all_zero.dat', 'w') as fop:
        for item in all0_data:
            fop.write(str(item['lon']).ljust(7))
            fop.write(str(item['lat']).ljust(7))
            for t in item['thick']:
                fop.write(str(format(t, '.4f')).ljust(5))
            fop.write('\n')
    with open('del_zero.dat', 'w') as fop:
        for item in d0_data:
            fop.write(str(item['lon']).ljust(7))
            fop.write(str(item['lat']).ljust(7))
            for t in item['thick']:
                fop.write(str(format(t, '.4f')).ljust(11))
            fop.write('\n')
    with open('all.dat', 'w') as fop:
        for item in all_data:
            fop.write(str(item['lon']).ljust(7))
            fop.write(str(item['lat']).ljust(7))
            for t in item['thick']:
                fop.write(str(format(t, '.4f')).ljust(11))
            fop.write('\n')
    with open('time.dat', 'w') as fop:
        for item in time:
            fop.write(str(item).ljust(5))

    return time, all_data


def con_icefile(time_file, data_file, ice_file):
    time_file = str(time_file)
    data_file = str(data_file)
    ice_file =str(ice_file)
    with open(time_file, 'r') as fip:
        f = fip.read().split()
        time = [float(element) for element in f]
        # print(time)
    with open(data_file, 'r') as fip:
        data = list()
        f = fip.readlines()
        # print(f)
        for item in f:
            i = [float(ele) for ele in item.split()]

            data.append(i)
        print(data)

    with open(ice_file, 'w') as fop:
        fop.write(str(len(data)) + '\n\n')
        for item in data:
            fop.write('10 0 6\n')
            fop.write(str(item[0]) + ' ' + str(90 - item[1]) + ' 0.5\n')
            fop.write(str(max(item[2:])) + '\n')
            fop.write(str(time[-1]) + ' ' + str(len(time) - 1) + '\n')
            for t in time:
                fop.write(str(t) + ' ')
            fop.write('\n')
            # for thick in item[2:]:
            #     fop.write(str(thick) + ' ')
            for i in range(len(item)-1, 1, -1):
                fop.write(str(item[i]) + ' ')
            fop.write('\n\n\n')


i7g_time, i7g_data = readi7g('./nc')
con_icefile('time.dat', 'del_zero.dat', 'ice7g_taboo.dat')
