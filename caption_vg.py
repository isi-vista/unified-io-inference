import argparse
import json
import os
from collections import defaultdict
from typing import List, Dict

from PIL import Image
from uio import runner
from uio.runner import CAPTIONING_PROMPT
from uio.configs import CONFIGS
import numpy as np
from absl import logging
import warnings
from itertools import islice
from pathlib import Path
# flax kicks up a lot of future warnings at the moment, ignore them
warnings.simplefilter(action='ignore', category=FutureWarning)

# To see INFO messages from `ModelRunner`
logging.set_verbosity(logging.INFO)


def main():
  parser = argparse.ArgumentParser()
  parser.add_argument("model_size", choices=list(CONFIGS))
  parser.add_argument("model_weights")
  parser.add_argument("vg_data_path")
  parser.add_argument("output_file")
  parser.add_argument("sample_count")
  parser.add_argument("--prompts", help="Path to text file listing alternative prompts")

  args = parser.parse_args()
  output_file = Path(args.output_file)
  if output_file.exists():
    os.remove(output_file)
  model = runner.ModelRunner(args.model_size, args.model_weights)
  prompts_list = []

  vg_data_path = Path(args.vg_data_path)
  if not vg_data_path.exists():
    raise RuntimeError(f"Could not find VG data directory at {vg_data_path}.")
  vg_images_path = vg_data_path.joinpath("images")
  vg_captions_path = vg_data_path.joinpath("region_descriptions.json")
  if not vg_images_path.exists():
    raise RuntimeError(f"Could not find VG image directory at {vg_images_path}.")

  # Create mapping from image IDs to VG captions
  image_ids_to_captions: Dict[str, List[str]] = defaultdict(list)
  if not vg_captions_path.exists():
    logging.warning(
      f"Could not find VG region descriptions at {vg_captions_path}; will not be logged."
    )
  else:
    logging.info("Creating image to description mapping...")
    with open(vg_captions_path, 'r', encoding='utf-8') as in_json:
      captions_json = json.load(in_json)
    for image_regions in captions_json:
      image_id = image_regions["id"]
      regions_list = image_regions["regions"]
      # Use the description(s) from the region that covers the most area
      largest_area = 0
      largest_area_descriptions = []
      for region_description in regions_list:
        width, height = region_description["width"], region_description["height"]
        region_area = width * height
        if region_area > largest_area:
          largest_area = region_area
          largest_area_descriptions = [region_description["phrase"]]
        elif region_area == largest_area:
          largest_area_descriptions.append(region_description["phrase"])
      image_ids_to_captions[str(image_id)] = largest_area_descriptions

  if args.prompts:
    prompts_path = Path(args.prompts)
    if prompts_path.exists():
      logging.info("Loading prompts from %s...", prompts_path)
      with open(prompts_path, 'r', encoding='utf-8') as prompts:
        prompts_list = prompts.readlines()
    else:
      logging.warning(
        "Prompts path %s doesn't exist. Skipping captions from alternative prompts.", args.prompts
      )

  logging.info(f"Captioning images from {vg_data_path}...")
  for sample_image_file in islice(vg_images_path.iterdir(), 0, int(args.sample_count)):
    if sample_image_file.suffix == ".jpg":
      image_id = sample_image_file.stem
      image_descriptions = " ".join(image_ids_to_captions[image_id])
      with Image.open(sample_image_file) as img:
        image = np.array(img.convert('RGB'))
      primary_output = model.vqa(image, CAPTIONING_PROMPT)
      all_output = {CAPTIONING_PROMPT: primary_output}
      logging.info(f"\n{image_id}\n{CAPTIONING_PROMPT}\n{image_descriptions}\n{primary_output['text']}\n")
      for alt_prompt in prompts_list:
        formatted_prompt = alt_prompt.strip('\n')
        output = model.vqa(image, formatted_prompt)
        all_output[formatted_prompt] = output
        output_text = output["text"]
        logging.info(f"\n{image_id}\n{formatted_prompt}\n{image_descriptions}\n{output_text}\n")

      with open(output_file, 'a') as of:
        for prompt, caption_output in all_output.items():
          output_text = caption_output["text"]
          of.write(f"{image_id}\t{prompt}\t{image_descriptions}\t{output_text}\n")


if __name__ == "__main__":
  main()
