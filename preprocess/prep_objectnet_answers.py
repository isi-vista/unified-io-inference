"""Create the answer key using the ObjectNet dataset."""
from argparse import ArgumentParser
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
			"--mapping-file",
			required=True,
			type=Path,
			help="File mapping folder name to class name.",
	)

	parser.add_argument(
		"--images-dir", required=True, type=Path, help="Input directory containing objectnet images."
	)

	parser.add_argument(
			"--output-file", required=True, type=Path, help="Output file containing the answer key."
	)

	args = parser.parse_args()
	images_dir = args.images_dir
	output_file = args.output_file
	
	with args.classes_file.open('r') as fp:
		classes_dict = json.load(fp)

	classes_enum = {class_name: class_id for class_id, class_name in enumerate(classes_dict['classes'])}

	with args.mapping_file.open('r') as fp:
		mapping_dict = json.load(fp)

	answer_key = {}
	for filetype in IMG_FILETYPES:
		for image_file in sorted(images_dir.rglob(filetype)):
			folder_name = image_file.parent.name
			class_name = mapping_dict[folder_name]
			answer_key[image_file.name] = classes_enum[class_name]
	
	with output_file.open('w') as fp:
		json.dump(answer_key, fp)
	

if __name__ == "__main__":
	main()
