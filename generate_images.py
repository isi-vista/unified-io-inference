#!python3
# Prompt unified-io-inference for image labels
# Usage: (activate virtual env, e.g. ". activate uioi &&"
# python ./generate_images.py xl sl.bin $PROMPTS_FILE $OUTPUT_DIR
import matplotlib.pyplot as plt
import argparse
import io
import json
import os
from PIL import Image, ImageDraw, ImageFont
from uio import runner
from uio.configs import CONFIGS
from uio import utils
import numpy as np
import spacy
from absl import logging
import warnings
from itertools import islice
from pathlib import Path
from datetime import datetime
# flax kicks up a lot of future warnings at the moment, ignore them
warnings.simplefilter(action='ignore', category=FutureWarning)
# To see INFO messages from `ModelRunner`
logging.set_verbosity(logging.INFO)

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument("model_size", choices=list(CONFIGS))
  parser.add_argument("model_weights")
  parser.add_argument("prompts_file")
  parser.add_argument("output_dir")
  args = parser.parse_args()
  output_dir = Path(args.output_dir)
  if not output_dir.exists():
    print(f"Output dir not found: {args.output_dir}")
    exit()

  model = runner.ModelRunner(args.model_size, args.model_weights)
  logging.info(f"Prompts: {args.prompts_file}\nOutput Dir: {args.output_dir}")
# read all the alternate prompts file JSON:
  prompts_file = open(f"{args.prompts_file}")
  prompts_data = json.load(prompts_file)
  logging.info(f"prompts_data: {prompts_data}")

  #TODO: read through prompts.  only generate single fixed image currently
  generated = model.image_generation("red and white stripes", num_decodes=1)
  print(f"Keys: {generated.keys()}")
  g_score = generated["score"]
  print(f"SCORE: {g_score}")
  g_image = generated["image"][0]
  print(f"Type: {type(g_image)}")
  print(f"Shape: {g_image.shape}")
  print(f"dtype: {g_image.dtype}")

  fig, ax = plt.subplots()
  ax.set_xticklabels([])
  ax.set_yticklabels([])    
  ax.imshow(g_image)
  plt.savefig(f"{args.output_dir}/generated_image.png")
  exit()

if __name__ == "__main__":
  main()
