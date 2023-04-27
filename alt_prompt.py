#!python3
# Prompt unified-io-inference for image labels
# Usage: (activate virtual env, e.g. ". activate uioi &&"
# python ./alt_prompt.py xl sl.bin $IMAGE_DIR $OUTPUT_FILE $SAMPLE_COUNT $PROMPTS_FILE
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
  parser.add_argument("image_dir")
  parser.add_argument("output_file")
  parser.add_argument("sample_count")
  parser.add_argument("prompts_file")
  args = parser.parse_args()
  image_dir = args.image_dir
  sample_count = int(args.sample_count)
  model = runner.ModelRunner(args.model_size, args.model_weights)
  logging.info(\
    f"Image Dir: {image_dir} Output: {args.output_file} SC: {sample_count} Prompts: {args.prompts_file}")

# read all the alternate prompts file JSON:
  prompts_file = open(f"{args.prompts_file}")
  prompts_data = json.load(prompts_file)
  logging.info(f"prompts_data: {prompts_data}")

# write to the output file for each response:
  with open(args.output_file, 'a') as output_file:
    output_file.write(f"Image Labeling by unified-io-inference on {datetime.now()}\t{Path(__file__)}\n")

# process all JPGs in image_dir
    images = Path(image_dir).glob("*.jpg")
    sorted_images = sorted(images, key = lambda x: os.stat(x).st_size * -1)

    for image_path in sorted_images:
      logging.info(f"Processing image: {image_path}\tsize: {os.stat(image_path).st_size}")
      with Image.open(image_path) as img:
        image = np.array(img.convert('RGB'))
        for prompt in prompts_data["prompts"]:
          output = model.vqa(image, prompt)
          output_text = output["text"]
          output_file.write(f"{image_path}\t{prompt}\t{output_text}\n")
          output_file.flush()

if __name__ == "__main__":
  main()
