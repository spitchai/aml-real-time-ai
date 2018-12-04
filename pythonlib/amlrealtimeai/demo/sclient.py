import requests
from amlrealtimeai.client import PredictionClient
import argparse

parse = argparse.ArgumentParser(description='AML inferencing client')
parse.add_argument('IP', type=str, help='IP of the FPGA runtime node')
parse.add_argument('path', type=str, help='Path to image that need to inferenced')
arg = parse.parse_args()
IP = arg.IP
path = arg.path

client = PredictionClient(IP, 80, False, '')
results = client.score_image(path)
#print(results)
trained_ds = requests.get("https://raw.githubusercontent.com/Lasagne/Recipes/master/examples/resnet50/imagenet_classes.txt").text.splitlines()
#for line in trained_ds:
#  print(line)

# map results [class_id] => [confidence]
results = enumerate(results)
#for line in results:
#  print(line)

# sort results by confidence
sorted_results = sorted(results, key=lambda x: x[1], reverse=True)
#for line in sorted_results:
#  print(line)

# print top 5 results
for top in sorted_results[:5]:
  print(trained_ds[top[0]], 'confidence:', top[1])
