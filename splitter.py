import argparse
import io
import json
import os
from os.path import exists
from PIL import Image, ImageDraw, ImageFont
from uio import runner
from uio.configs import CONFIGS
from uio import utils
import numpy as np
import spacy
from absl import logging
import warnings
import webdataset as wds
from itertools import islice
from pathlib import Path
# flax kicks up a lot of future warnings at the moment, ignore them
warnings.simplefilter(action='ignore', category=FutureWarning)

# To see INFO messages from `ModelRunner`
logging.set_verbosity(logging.INFO)

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument("vizwiz_file")
  parser.add_argument("output_dir")
  args = parser.parse_args()
  output_dir = args.output_dir
  if (not exists(output_dir)):
    logging.error(f"TODO check write capabilities.")
    quit()

  logging.info(f"Reading: {args.vizwiz_file}")
  vizwiz_file = open(f"{args.vizwiz_file}")
  vizwiz_data = json.load(vizwiz_file)
  print(f"VizWiz keys: {vizwiz_data.keys()}")
  print(f"Info: {vizwiz_data['info']}")
  images = vizwiz_data['images']

  for r in range(0, 10):
    image_batch = [i for i in images if int(i['id']) % 10 == r]
    output_file = os.path.join(output_dir, 'batch_' + str(r) + '.json')
    logging.info(f"Writing: {output_file}")
    with open(output_file, 'w') as f:
      batch = {"info":"batch_" + str(r),"images":image_batch}
      json.dump(batch, f)
    logging.info(f"Wrote: {output_file} Images: {len(image_batch)}")
  quit()

if __name__ == "__main__":
  main()
