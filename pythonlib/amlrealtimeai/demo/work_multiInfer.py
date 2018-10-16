import threading
import time
import requests
from client import PredictionClient
import pdb
import agrparse

meantime = []
tcount = 32
tper = 512

def worker(td):
    count = 0
    tt = 0
    path = '/home/srpitcha/images/dog.png'
    for i in range(tper):
        ts = time.time()
        count += 1
        client = PredictionClient('10.128.46.108', 80, False, '')
        results = client.score_image(path)
        te = time.time()
        tt += te-ts
    mtime = tt/count
    meantime.append(mtime)

if __name__ == '__main__':
  par = argparse.ArgumentParser()
  par.add_argument('IP', help='IP address of the ML runtime')
  arg = par.parse()
  tstart = time.time()
  thread_list = []
  for i in range(tcount):
    t = threading.Thread(target=worker, args=(i,))
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
