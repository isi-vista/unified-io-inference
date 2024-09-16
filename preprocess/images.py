from argparse import ArgumentParser
from pathlib import Path
import random
from uio.runner import IMAGE_TAGGING
from PIL import Image
from numpy import asarray

random.seed(0)

DEFAULT_QUESTION = IMAGE_TAGGING
IMG_FILETYPES = ['*.jpg','*.png']

def preprocess_images(images_dir: Path, n_samples = -1):
	uio_file_contents = []
	filepaths = []
	for filetype in IMG_FILETYPES:
		filepaths.extend(sorted(images_dir.rglob(filetype)))

	if n_samples > 0:
		filepaths = random.sample(filepaths, n_samples)

	for input_file in filepaths:
		uio_line = f"{input_file.absolute()}:{DEFAULT_QUESTION}"
		uio_file_contents.append(uio_line)

	return uio_file_contents 

def main():
	parser = ArgumentParser(__doc__)
	parser.add_argument(
			"--input-dir", required=True, type=Path, help="Input directory containing images."
	)

	parser.add_argument(
			"--output-file",
			required=True,
			type=Path,
			help="Output file to write the unified inputs.",
	)

	parser.add_argument("--n-samples", type=int, help="Number of samples to use. All images are used if this argument is not specified.")

	args = parser.parse_args()
	input_dir = args.input_dir

	uio_file_contents = preprocess_images(input_dir, n_samples= args.n_samples)
	with args.output_file.open('w') as fp:
		fp.write('\n'.join(uio_file_contents))

if __name__ == "__main__":
	main()
