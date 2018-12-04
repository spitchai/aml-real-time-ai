import threading
import os
import time
import requests
import glob
import imghdr
import argparse
from amlrealtimeai.client import PredictionClient
from shutil import copyfile

import pdb

def worker(IP, path):
  datadir = os.path.expanduser(path)
  pass_files= glob.glob(os.path.join(datadir, 'pass', '*.jpg'))
  fail_files = glob.glob(os.path.join(datadir, 'fail', '*.jpg'))
  print("Pass files")
  for image in pass_files:
    client = PredictionClient(IP, 80, False, '')
    results = client.score_image(image)
    print(image, results)
    if (results < 0.5):
      pdb.set_trace()
      print(image, results)
  print("Fail files")
  for image in fail_files:
    client = PredictionClient(IP, 80, False, '')
    results = client.score_image(image)
    print(image, results)
    if (results >= 0.5):
      pdb.set_trace()
      print(image, results)

if __name__ == '__main__':
  parse = argparse.ArgumentParser(description='AML inferencing client')
  parse.add_argument('IP', type=str, help='IP of the FPGA runtime node')
  parse.add_argument('path', type=str, help='Path to image that need to inferenced')
  arg = parse.parse_args()
  IP = arg.IP
  path = arg.path
  worker(IP, path)
