import threading
import os
import time
import requests
import glob
import imghdr
import argparse
from client import PredictionClient
from shutil import copyfile

import pdb

def cp(src_file, dst_folder):
  fname = os.path.split(src_file)
  dfile = os.path.join(dst_folder, fname[1])
  copyfile(src_file, dfile)

def worker(IP, path):
  datadir = os.path.expanduser(path)
  pass_files= glob.glob(os.path.join(datadir, 'pass', '*.jpg'))
  fail_files = glob.glob(os.path.join(datadir, 'fail', '*.jpg'))
  dest_pass = os.path.join(datadir, 'output', 'pass')
  dest_fail = os.path.join(datadir, 'output', 'fail')
  print("Pass files")
  for image in pass_files:
    client = PredictionClient(IP, 80, False, '')
    results = client.score_image(image)
    if (results >= 0.5):
      print("PASS", image, results)
      cp(image, dest_pass)
    else:
      print("FAIL", image, results)
      cp(image, dest_fail)
  print("Fail files")
  for image in fail_files:
    client = PredictionClient(IP, 80, False, '')
    results = client.score_image(image)
    if (results < 0.5):
      cp(image, dest_fail)
    else:
      print(image, results)
      cp(image, dest_pass)

if __name__ == '__main__':
  parse = argparse.ArgumentParser(description='AML inferencing client')
  parse.add_argument('IP', type=str, help='IP of the FPGA runtime node')
  parse.add_argument('path', type=str, help='Path to image that need to inferenced')
  arg = parse.parse_args()
  IP = arg.IP
  path = arg.path
  worker(IP, path)

