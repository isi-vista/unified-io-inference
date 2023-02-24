"""Pulls images from urls provided from Visual Genome's image_data.json.

Requires the `wget` Python package to run.
"""
import argparse
import json
import logging
import os
import traceback
import wget
from pathlib import Path

logging.basicConfig(level=logging.INFO)


def main(data_path: Path, dryrun: bool):
    """Pulls images from urls provided in `visual_genome_python_driver/data/image_data.json.
    
    Prerequisites:
    - Cloning the VG python driver (https://github.com/ranjaykrishna/visual_genome_python_driver)
      and running `getImageData.sh` to download `image_data.json`
    - Installing the `wget` Python package
    
    Input:
        `data_path`: the path where `image_data.json` is located; this is also where the images will be saved
        `dryrun` (optional): prints where the data will be saved and how many images will be pulled
    
    Images will be saved in `<data_path>/images`.
    """
    image_data_path = data_path.joinpath("image_data.json")
    if not image_data_path.exists():
        logging.error(
            "Could not locate image data file %s. " +
            "Check that you have the correct `data_dir` and that you have downloaded image_data.json.",
            image_data_path
        )
    with open(data_path.joinpath("image_data.json"), 'r', encoding='utf-8') as in_json:
        image_json = json.load(in_json)
    bad_urls_count = 0
    treat_as_completed = True
    image_url_count = 0
    downloaded_images_count = 0
    images_dir = data_path.resolve().joinpath("images")
    images_dir_str = str(images_dir)
    saved_image_ids = set()
    saved_images_count = 0
    if Path(images_dir).exists():
        # Find the IDs of each image downloaded
        for image_file in images_dir.iterdir():
            try:
                image_int = int(image_file.stem)
                saved_image_ids.add(image_int)
            except ValueError:
                logging.warning("Couldn't convert `%s` (%s) to int", image_file.stem, image_file)
        saved_images_count = len(saved_image_ids)
    else:
        os.makedirs(images_dir)
    if dryrun:
        logging.info("The images would be saved to %s", images_dir)
    else:
        logging.info("Saving images to %s...", images_dir)
    for image in image_json:
        image_url = image.get("url")
        if image_url:
            image_id = image_url.rsplit("/", 1)[1].split(".")[0]
            image_id_int = int(image_id)
            if dryrun:
                image_url_count += 1
            elif image_id_int not in saved_image_ids:
                try:
                    wget.download(image_url, out=images_dir_str)
                    downloaded_images_count += 1
                except Exception:
                    logging.warning("Failed to pull image from %s", image_url)
                    logging.info("Message: %s", traceback.format_exc())
                    bad_urls_count += 1
        if bad_urls_count >= 10:
            logging.warning("Several images failed to pull; there's probably something weird going on.")
            treat_as_completed = False
            break

    if treat_as_completed:
        if dryrun:
            logging.info("Done")
            logging.info("Total urls: %d", image_url_count)
            logging.info("Would download %d more images", image_url_count - saved_images_count)
        else:
            logging.info("Done saving images to %s", images_dir)
            logging.info("Images successfully pulled: %d", downloaded_images_count)
            logging.info("Images that failed to download: %d", bad_urls_count)


if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("--data-path", help="Path to the Visual Genome data")
    arg_parser.add_argument(
        "--dryrun",
        help="If dryrun, will only print the output path and url stats",
        action="store_true"
    )
    args = arg_parser.parse_args()
    main(data_path=Path(args.data_path), dryrun=args.dryrun)
