import threading
import time
import requests
from amlrealtimeai.client import PredictionClient
import pdb
import argparse

meantime = []
tcount = 1
tper = 10

def worker(IP, path):
    count = 0
    tt = 0
    #path = '/home/srpitcha/images/dog.png'
    for i in range(tper):
        ts = time.time()
        count += 1
        client = PredictionClient(IP, 80, False, '')
        results = client.score_image(path)
        te = time.time()
        tt += te-ts
    mtime = tt/count
    meantime.append(mtime)

if __name__ == '__main__':
  parse = argparse.ArgumentParser(description='AML inferencing client')
  parse.add_argument('IP', type=str, help='IP of the FPGA runtime node')
  parse.add_argument('path', type=str, help='Path to image that need to inferenced')
  arg = parse.parse_args()
  IP = arg.IP
  path = arg.path

  tstart = time.time()
  thread_list = []
  for i in range(tcount):
    t = threading.Thread(target=worker, args=(IP, path,))
    t.start()
    thread_list.append(t)

  for t in thread_list:
    t.join()

  s = 0
  for i in meantime:
    print('mean time list:', i)
    s += i
  ave_time = s/len(meantime)
  tend = time.time()
  ttotal = tend - tstart
  nettime = ttotal/(tcount * tper)
  print('list len', len(meantime))
  print('average time', ave_time)
  print('total time:', ttotal, 'net time:', nettime)
