import argparse
from absl import logging
from pathlib import Path
import warnings
# flax kicks up a lot of future warnings at the moment, ignore them
warnings.simplefilter(action='ignore', category=FutureWarning)

# To see INFO messages from `ModelRunner`
logging.set_verbosity(logging.INFO)

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument("--predictions", type=Path, required=True, help="Path to the input file containing image IDs and predicted labels." )
  parser.add_argument("--gold-labels", type=Path, required=True, help = "File containing the solution strings.")
  parser.add_argument("--synsets", type=Path, required=True, help = "CSV file containing class names.")

  args = parser.parse_args()
  pred_file = args.predictions
  gold_file = args.gold_labels
  synset_file = args.synsets
  
  synsets = {}
  with synset_file.open('r') as fp:
    for line in fp.readlines():
      synset_id = line[:line.index(' ')]
      synset_strings = [entry.strip() for entry in line[line.index(' '):].split(',')]
      synsets[synset_id] = synset_strings

  gold_labels = {}
  with gold_file.open('r') as fp:
    for line in fp.readlines():
      image_id, solution_string = line.strip().split(',')
      synset_id = solution_string.strip().split(' ')[0]
      gold_labels[image_id] = synset_id

  n_correct = 0
  n_preds = 0
  with pred_file.open('r') as fp:
    for line in fp.readlines():
      image_path, _,pred_label = line.strip().split(':')
      image_id = Path(image_path).stem
      n_preds+=1
      
      gold_synset = synsets[gold_labels[image_id]]
      if pred_label in gold_synset:
        n_correct+=1


  logging.info(f"Accuracy of the predictions in file `{pred_file}`: {n_correct*100/n_preds:.2f}% ({n_correct}/{n_preds}) ")

if __name__ == "__main__":
  main()
