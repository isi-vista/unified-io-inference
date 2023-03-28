"""Create the answer key using the ObjectNet dataset."""
from argparse import ArgumentParser
import csv
import json
from pathlib import Path

IMG_FILETYPES = ['*.jpg','*.png']

def main():
	parser = ArgumentParser(__doc__)

	parser.add_argument(
			"--classes-file",
			required=True,
			type=Path,
			help="Input file containing the classes dict.",
	)

	parser.add_argument(
			"--pred-file",
			required=True,
			type=Path,
			help="File containing Unified-IO predictions.",
	)

	parser.add_argument(
			"--output-file", required=True, type=Path, help="Output file containing predictions in the format expected by the objectnet scorer."
	)

	args = parser.parse_args()
	
	with args.classes_file.open('r') as fp:
		classes_dict = json.load(fp)

	classes_enum = {class_name: class_id for class_id, class_name in enumerate(classes_dict['classes'])}

	predictions = []
	with args.pred_file.open('r') as fp:
		for line in fp.readlines():
			image_fpath, _, class_name = line.split(':')

		predictions.append([Path(image_fpath).name, classes_enum[class_name], 1.0])
	
	with open(args.output_file, 'w') as csvOut:
		csvwriter = csv.writer(csvOut, delimiter=',')
		for predictImg in predictions:
			csvwriter.writerow(predictImg)
	

if __name__ == "__main__":
	main()
