#!/usr/bin/env python3
# Generate claims from text files containing questions and answers.
# Usage:
# python3 ./generate_claims.py /my_path/text.txt,/my_path/tsv.tsv /my_path/out_myway.json
import argparse
import json
import os
from collections import defaultdict
from typing import List, Dict
from pathlib import Path

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument("tsv_files", help="Comma-separated list of input file paths")
  parser.add_argument("output_file", default="generated_claims.json")
  args = parser.parse_args()

  output_file = Path(args.output_file)
  print(f"OUTPUT: {output_file}")
  if output_file.suffix != ".json":
    print(f"{output_file.suffix} is not JSON.\nExiting...")
    exit()
  if output_file.exists():
    print(f"Output file exists: {output_file}\nExiting...")
    exit()

  claims = []
  for tsv in args.tsv_files.split(','):
    tsv_file = Path(tsv)
    print(f"INPUT: {tsv}")
    with open(tsv_file) as f:
      for line in f:
        if line.count('\t') == 2:
          image_path, question, answer = line.split('\t')
          image_stem = Path(image_path).stem
          answer = answer.lower().strip()
          if answer.find('virus') >= 0 or answer.find('mask') >= 0:
            claims.append({"sentence":str(answer).strip(), \
              "associated_KEs": [], \
              "claim_id": f"claim_{image_stem}_{len(claims)}", \
              "claim_semantics": [], \
              "claim_span_end": 0, \
              "claim_span_start": 0, \
              "claim_span_text": answer, \
              "claimbuster_score": 0.0, \
              "claimer_affiliation": "", \
              "claimer_affiliation_identity_qnode": "", \
              "claimer_affiliation_type_qnode": "", \
              "claimer_debug": "", \
              "claimer_end": 2762, \
              "claimer_ke": [], \
              "claimer_ke_qnode": [], \
              "claimer_ke_typeqnode": [], \
              "claimer_qnode": "", \
              "claimer_score": 0.0, \
              "claimer_search_key": "", \
              "claimer_start": 0, \
              "claimer_text": "", \
              "claimer_type_qnode": "", \
              "end_char": 0, \
              "entity": "PER.Professional.Scientist", \
              "equivalent_claims": [], \
              "equivalent_claims_text": "", \
              "final_claim_score": 0.0, \
              "generation": "GAIA Unified-IO-Inference", \
              "lan": "EN", \
              "location": "Indoors", \
              "news_author": "", \
              "news_url": "", \
              "qnode_x_variable_identity": "", \
              "qnode_x_variable_type": "", \
              "refuting_claims": [], \
              "refuting_claims_text": "", \
              "render_text": [], \
              "segment_id": "", \
              "sentence": answer, \
              "sentence_L": "\"", \
              "sentence_M": answer, \
              "sentence_R": ".\"", \
              "source": image_stem, \
              "stance": "Affirm", \
              "start_char": 0, \
              "sub_topic": "Who can contract COVID-19", \
              "supporting_claims": [], \
              "supporting_claims_text": "", \
              "template": question, \
              "time_attr": "", \
              "time_end_earliest": "", \
              "time_start_earliest": "", \
              "time_start_latest": "", \
              "topic": "Contracting the virus", \
              "topic_score": 0.0, \
              "x_end": 0, \
              "x_ke": [], \
              "x_ke_qnode": [], \
              "x_ke_typeqnode": [], \
              "x_start": 0, \
              "x_variable": ""})

  with open(output_file, 'w') as f:
    container = {"claims":claims}
    json.dump(container, f, indent=2)

  print(f"Wrote: {output_file}\nDone.")

if __name__ == "__main__":
  main()
