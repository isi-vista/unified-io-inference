# Evaluating Imagenet predictions
Evaluating imagenet predictions requires two additional files that can be downloaded as a part of ImageNet -

- `LOC_synset_mapping.txt`: The mapping between the 1000 synset id and their descriptions. For example, Line 1 says `n01440764 tench, Tinca tinca` means this is class 1, has a synset id of `n01440764`, and it contains the fish `tench`.
- `LOC_train_solution.csv` and `LOC_val_solution.csv` -  Each file contains two columns:
    - ImageId: the id of the train/val image, for example `n02017213_7894` or `ILSVRC2012_val_00048981`
    - PredictionString: the prediction string is a space delimited of 5 integers. For example, `n01978287 240 170 260 240` means it's label `n01978287`, with a bounding box of coordinates (x_min, y_min, x_max, y_max). Repeated bounding boxes represent multiple boxes in the same image: `n04447861 248 177 417 332 n04447861 171 156 251 175 n04447861 24 133 115 254`

The evaluation script can be run using the following command - 

`python score/imagenet.py --predictions PREDICTIONS_FILE --gold-labels PATH_TO_SOLUTION --synsets PATH_TO_SYNSETS`