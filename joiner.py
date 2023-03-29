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
  parser.add_argument("batch_file")
  parser.add_argument("output_dir")
  args = parser.parse_args()
  output_dir = args.output_dir
  if (not exists(output_dir)):
    logging.error(f"TODO check write capabilities.")
    quit()

  logging.info(f"Reading: {args.batch_file}")
  batch_file = open(f"{args.batch_file}")
  batch_data = json.load(batch_file)
  captions = []
  for b in batch_data:
    logging.info(f"Reading: {b}")
    b_file = open(b)
    b_captions = json.load(b_file)
    captions.extend(b_captions)

  logging.info(f"Total captions: {len(captions)}")
  captions.sort(key=lambda x: int(x['image_id']))
  output_file = os.path.join(output_dir, 'joined.json')
  logging.info(f"Writing: {output_file}")
  with open(output_file, 'w') as f:
    json.dump(captions, f)

  logging.info(f"Wrote: {output_file} Images: {len(captions)}")
  quit()

if __name__ == "__main__":
  main()
