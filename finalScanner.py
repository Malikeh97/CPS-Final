#!/usr/bin/python3

import time
import csv
from bluepy.btle import Scanner, DefaultDelegate

class ScanDelegate(DefaultDelegate):
    def init(self):
        DefaultDelegate.init(self)


    def HandleDiscovery(self,dev,new_dev,new_dat):
        if new_dev:
            pass
        if new_dat:
            pass
print('hello from nordic')
scanner = Scanner().withDelegate(ScanDelegate())

time_diff = 0
first_time = 1

fileName = input('Enter file name:')
distance = input('Enter distance in meters:')
num = 0
with open(fileName,mode='w', newline='') as newFile:
  fieldNames = ['uuid', 'distance', 'rssi']
  newFileWriter = csv.DictWriter(newFile, fieldnames = fieldNames)
  newFileWriter.writeheader()
  while num < 1000:
      try:

          devices = scanner.scan(0.35, passive = True)
  #        print("Amount of Devices = "+str(len(devices)))
          for ii in devices:
  #            print(ii.addr)
              if ii.addr == u'd6:fb:b2:5e:83:c5':
                  num = num+1;
                  print("Device %s, RSSI=%d dB" % (ii.addr,ii.rssi))
                  newFileWriter.writerow({'uuid' : 'd6:fb:b2:5e:83:c5', 'distance' : distance, 'rssi': ii.rssi})

                  if first_time == 1:
                      first_time = 0
                      pass
                  else:
                      time_diff = time.time()-time_prev


                  time_prev = time.time()
                  rssi_prev = ii.rssi
                  continue

      except:
          continue

