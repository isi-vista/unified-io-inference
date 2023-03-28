"""
Script to remove broders from ObjectNet images.

The ObjectNet dataset contains images that have a 1px red border that needs to be removed 
"""
from argparse import ArgumentParser
import os
from pathlib import Path
from PIL import Image
from numpy import asarray

IMG_FILETYPES = ['*.jpg','*.png']

def main():
	parser = ArgumentParser(__doc__)
	parser.add_argument(
			"--input-dir", required=True, type=Path, help="Input directory containing objectnet images."
	)

	parser.add_argument(
			"--output-dir", type=Path, help="Output directory to store processed objectnet images."
	)

	args = parser.parse_args()
	input_dir = args.input_dir
	output_dir = args.output_dir

	for filetype in IMG_FILETYPES:
		for input_file in sorted(args.input_dir.rglob(filetype)):
			image = Image.open(input_file)
			data = asarray(image)
			borderless_data = data[1:-1, 1:-1]
			borderless_image = Image.fromarray(borderless_data)
			
			relative_path = os.path.relpath(input_file, input_dir)
			output_fpath = output_dir / relative_path
			output_fpath.parent.mkdir(parents=True, exist_ok=True)
				
			borderless_image.save(output_fpath)


if __name__ == "__main__":
	main()
