import threading
import os
import time
import requests
import glob
import imghdr
import argparse
from client import PredictionClient
import pdb

meantime = []
tcount = 1
tper = 10



def worker(IP, path, trainedDs):
  count = 0
  tt = 0
  datadir = os.path.expanduser(path)
  cat_files = glob.glob(os.path.join(datadir, 'pass', '*.jpg'))
  dog_files = glob.glob(os.path.join(datadir, 'fail', '*.jpg'))
  pdb.set_trace()
  for image in cat_files[:5]:
    ts = time.time()
    count += 1
    client = PredictionClient(IP, 80, False, '')
    results = client.score_image(image)
    results = enumerate(results)
    sorted_results = sorted(results, key=lambda x: x[1], reverse=True)
    for top in sorted_results[:5]:
      print(trainedDs[top[0]], 'confidence:', top[1])
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
  trainedDs = requests.get("https://raw.githubusercontent.com/Lasagne/Recipes/master/examples/resnet50/imagenet_classes.txt").text.splitlines()
  worker(IP, path, trainedDs)

