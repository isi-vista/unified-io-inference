
## Docker
To build a docker image:
```bash
docker build -t unified-io-inference .
```

To build using named Dockerfile:
```bash
docker build -t unified-io-inference:vizwiz -f VizWiz.Dockerfile .
```

To run captioning of the CC12M dataset using Unified-IO:
```bash
docker run -it --gpus=1 -e WEBDATASET_FILE=/input/00000.tar -v /nas/gaia02/data/paper2023/cc12m/images:/input -v /nas/gaia02/users/napiersk/github/feb-14/unified-io-inference/output:/output -e SAMPLE_COUNT=500 unified-io-inference
```

To run vizwiz (train|val|test):
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

To run VizWiz scoring (work in progress)
```bash
docker run -it --gpus=1 -v /nas/gaia02/data/paper2023/vizwiz/data/images/val:/images \
 -v ${OUTPUT}:/output \
 -v /nas/gaia02/data/paper2023/vizwiz/data/annotations:/input \
 -e VIZWIZ_FILE=/input/val.json \
 --entrypoint /bin/bash unified-io-inference:vizwiz
...
# export PYTHONPATH="/root/vizwiz/vizwiz-caption"
# bash -c ". activate vizwiz && python ./eval-vizwiz.py"
```

To run joiner (wip)
```bash
docker run -it --gpus "device=0" \
 -v ${BATCHES}:/batches:ro \
 -v ${OUTPUT}:/output \
 --entrypoint /bin/bash unified-io-inference:vizwiz
...
# bash -c ". activate uioi && python ./joiner.py /batches/batch.json /output"
```
