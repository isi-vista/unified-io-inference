
## Docker

### Build
To build a docker image (default image processes CC12M dataset):
```bash
docker build -t unified-io-inference .
```

To build using named Dockerfile (such as for VizWiz custom Dockerfile):
```bash
docker build -t unified-io-inference:vizwiz -f VizWiz.Dockerfile .
docker build -t unified-io-inference:alt-prompts -f Alt_Prompts_Dockerfile .
```

### Run
Alternate Prompts:
```bash
export IMAGE_DIR=/nas/gaia02/users/napiersk/data/LDC2021E11_AIDA_Phase_3_Practice_Topic_Source_Data_V2.0/data/jpg/jpg
export OUTPUT_DIR=/nas/gaia02/users/napiersk/github/april19/unified-io-inference/output/alt-prompts
export SAMPLE_COUNT=10
export PROMPTS_FILE=/images/alternative_prompts.json
docker run -it --gpus="device=0" \
-e IMAGE_DIR=/images \
-e OUTPUT_DIR=/output \
-e SAMPLE_COUNT=$SAMPLE_COUNT \
-e PROMPTS_FILE=$PROMPTS_FILE \
-v ${IMAGE_DIR}:/images:ro \
-v ${OUTPUT_DIR}:/output \
unified-io-inference:alt-prompts
```

Caption CC12M:
```bash
export HOST_INPUT_DIR=/nas/gaia02/data/paper2023/cc12m/images
export HOST_OUTPUT_DIR=/someoutputpathonthehost
docker run -it --gpus=1 \
-e WEBDATASET_FILE=/input/00000.tar \
-v ${HOST_INPUT_DIR}:/input \
-v ${HOST_OUTPUT_DIR}:/output \
-e SAMPLE_COUNT=500 unified-io-inference
```

Split VizWiz dataset into batches:
```bash
docker run -it --gpus "device=0" \
 -v ${INPUT}:/input:ro \
 -v ${OUTPUT}:/output \
 --entrypoint /bin/bash unified-io-inference:vizwiz
...
# export PYTHONPATH="/root/vizwiz/vizwiz-caption"
# bash -c ". activate vizwiz && python ./splitter.py"
```

Caption VizWiz (train|val|test):
TODO: specify device id for each batch.
```bash
export DATA=test
export BATCH=_0
docker run -it --gpus "device=" \
 -v /nas/gaia02/data/paper2023/vizwiz/data/images/${DATA}:/images \
 -v ${OUTPUT}:/output \
 -v /nas/gaia02/data/paper2023/vizwiz/data/annotations:/input \
 -e VIZWIZ_FILE=/input/${DATA}${BATCH}.json \
 -e SAMPLE_COUNT=800 \
 unified-io-inference:vizwiz
```

Join VizWiz results
```bash
docker run -it --gpus "device=0" \
 -v ${BATCHES}:/batches:ro \
 -v ${OUTPUT}:/output \
 --entrypoint /bin/bash unified-io-inference:vizwiz
...
# bash -c ". activate uioi && python ./joiner.py /batches/batch.json /output"
```
