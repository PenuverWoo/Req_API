import requests
import hashlib
import base64
from urllib.parse import quote
import matplotlib.pyplot as plt

from openpyxl import load_workbook
import openpyxl
from openpyxl.workbook import Workbook
import datetime
import numpy as np

from matplotlib.pyplot import MultipleLocator

import time, datetime

from twilio.rest import Client

class AutoReport():

    def __init__(self, _id, _room):
        # Request parameter test
        self.method = 'GET'
        self.url = 'saas.cleargrass.com'
        self.sub_url = '/v2/device/pheasant/data/fc/'
        # self.device_id = '761B5379295BA4BE6EA232E4DB029D43'
        # self.device_id = '2288A0374E9180D21068B10E9C859963' # Sawing id
        # self.device_id = 'A6461D1B394EBD0169FCD77AD777F11B' # AP ID
        # self.device_id = '5ACC0CFA5B88A513AE8EEDAFD91BF6BE' # Sawing
        self.device_id = _id # Woekshop
        print(self.device_id)
        # self.device_id = '93E54867A2CDB6A7A3BAF5BCDA1BA31E' # Ronnie
        # self.start = str(1572883200)
        # self.end = str(1572904800)
        self.offset = '0'
        self.limit = '50'
        self.timestamp = '0.111'
        self.token = '0bd48fd37ee444029d499a94470461fc'
        self.asc = 'false'
        self.key = 'ff3f2801c8d942b484431fcd386f5463'
        self.Daily_humidity = [str(_room),'Humidity', time.strftime('%Y-%m-%d')]
        self.Daily_temperature = [str(_room), 'Temperature', time.strftime('%Y-%m-%d')]
        self.Daily_pressure = [str(_room), 'Pressure',time.strftime('%Y-%m-%d')]
        self.timestamps = [str(_room),'Date', time.strftime('%Y-%m-%d')]



    def _Connect(self, start_Date, end_Date):
        # Init key signature parameter
        # end_Date = int(end_Date) + 1
        value = '{}?{}?{}{}&asc={}&end={}&limit={}&offset={}&start={}&timestamp={}&token={}&key={}'. \
            format(self.method, self.url, self.sub_url, self.device_id, self.asc, end_Date, self.limit, self.offset, start_Date, self.timestamp, self.token, self.key)

        # encode init key by sha256 -> base64 -> url_encode -> UpperCase
        self.Key_signature = quote(base64.b64encode(hashlib.sha256(value.encode('utf-8')).digest()), 'utf-8').upper()
        # print(self.Key_signature)

        # Request url
        url = 'https://{}{}{}?asc={}&device_id={}&end={}&key={}&limit={}&offset={}&start={}&timestamp={}&token={}' \
            .format(self.url, self.sub_url, self.device_id, self.asc, self.device_id, end_Date, self.Key_signature, self.limit, self.offset, start_Date, self.timestamp, self.token)

        return requests.get(url).json()

    # Get one day humidity, temperature and pressure data
    def getData(self, _date):
        self.timeArray = time.strptime(_date+' 00:00:00', "%Y-%m-%d %H:%M:%S")
        self.timeStamp = int(time.mktime(self.timeArray))
        self.Daily_humidity.append(_date)
        self.Daily_temperature.append(_date)
        self.Daily_pressure.append(_date)
        self.timestamps.append(_date)
        for j in range(4):
            data = self._Connect(str(self.timeStamp+(j*21600)), str(self.timeStamp+((j+1)*21600)))
            # print(data)
            self.data_Len = data['data']['total']
            for i in range(1, self.data_Len):
                # print(self.data_Len, i, j)
                if time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(data['data']['data'][self.data_Len - i]['timestamp'])) in self.timestamps: # Delete repeat data bug
                    # print(data['data']['data'][self.data_Len - i]['timestamp'])
                    # print('Error{}'.format(i))
                    pass
                # elif i is 1 and j is 0:
                #     # self.timestamps.append(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(data['data']['data'][self.data_Len - i]['timestamp'])))
                #     self.Daily_humidity.append(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(data['data']['data'][self.data_Len - i]['timestamp'])))
                #     self.Daily_temperature.append(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(data['data']['data'][self.data_Len - i]['timestamp'])))
                #     self.Daily_pressure.append(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(data['data']['data'][self.data_Len - i]['timestamp'])))
                else:                                                                                           # Catch these four data
                    self.Daily_humidity.append(data['data']['data'][self.data_Len - i]['humidity'])
                    self.Daily_temperature.append(data['data']['data'][self.data_Len - i]['temperature'])
                    self.Daily_pressure.append(data['data']['data'][self.data_Len - i]['pressure'])
                    self.timestamps.append(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(data['data']['data'][self.data_Len - i]['timestamp'])))
        # print('H: ', self.Daily_humidity, '\nT: ', self.Daily_temperature, '\nP: ', self.Daily_pressure, '\nTime: ', self.timestamps)
        # print(len(self.Daily_humidity))
        # print(len(self.Daily_temperature))
        # print(len(self.Daily_pressure))
        # print(len(self.timestamps))
        self.saveXls()

        # f, axarr = plt.subplots(2, sharex=True)
        # f.suptitle('dsdsd')
        # axarr[0].plot(self.timestamps, self.Daily_humidity)
        # axarr[1].plot(self.timestamps, self.Daily_temperature, color='r')
        # plt.plot(self.Daily_humidity)

        # a = list(range(len(self.timestamps)))
        # plt.xticks(a, self.timestamps, rotation=70, fontsize=4)
        # my_x_ticks = np.arange(-5, 10, 1)
        # plt.xticks(my_x_ticks)
        # ax = plt.gca()
        # y_major_locator = MultipleLocator(10)
        #
        # ax.yaxis.set_major_locator(y_major_locator)


    def saveXls(self):

        wb = load_workbook('ht2.xlsx')
        wt = wb['T']
        # wt.append(self.timestamps)
        wt.append(self.Daily_temperature)
        wh = wb['H']
        # wh.append(self.timestamps)
        wh.append(self.Daily_humidity)
        wp = wb['P']
        # wp.append(self.timestamps)
        wp.append(self.Daily_pressure)
        wb.save("ht2.xlsx")
        wb.close()
        # print(len(self.timestamps))
        # print(len(self.Daily_temperature))
        # x = self.timestamps
        # y = self.Daily_temperature
        # plt.xticks( rotation=45)
        # # plt.xlim(0,10)
        # plt.plot(x, y, label='laji')
        # plt.show()




if __name__ == '__main__':

    id = {
        'Sawing': '5ACC0CFA5B88A513AE8EEDAFD91BF6BE',
        'AP': 'A6461D1B394EBD0169FCD77AD777F11B',
        'Woekshop': '2FFFE50729859F3C6D484388E4C714B4',
        'Ronnie': '93E54867A2CDB6A7A3BAF5BCDA1BA31E'
    }

    for j in id:
        for i in range(16, 17):  # Start day and (end day + 1)
            a = AutoReport(id[j], j)
            a.getData('2020-02-{}'.format(i))

