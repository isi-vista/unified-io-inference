### Generating Claims

Claims made be generated from question answering results.  
See the example in the ./test/answers.tsv

Example usage:
```
conda env create -f uioi.yml
conda activate uioi
python3 ./generate_claims.py ./test/answers.tsv ./test/claims.json
```

