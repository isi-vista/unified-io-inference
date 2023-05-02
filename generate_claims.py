#!/usr/bin/env python3
# Generate claims from text files containing questions and answers.
# Usage:
# python3 ./generate_claims.py /my_path/text.txt,/my_path/tsv.tsv /my_path/out_myway.json
import argparse
import json
import os
from collections import defaultdict
from typing import List, Dict
#from absl import logging
from pathlib import Path

def main():
#  with open("/nas/gaia02/users/napiersk/github/may01/unified-io-inference/single_claim.json") as claim_file:
#    parsed_claims = json.load(claim_file)
#    print(f"Claims keys: {parsed_claims.keys()}")
#    print(f"first claim: {parsed_claims['claims'][0].keys()}")
# JSON FORMAT:
#Claims keys: dict_keys(['claims'])
#first claim: dict_keys(
#['sentence', 'claim_span_text', 'claimbuster_score', 'claimer_end', 'start_char', 
#'time_end_earliest', 'claimer_debug', 'associated_KEs', 'claimer_ke', 'claim_span_end', 
#'claim_id', 'x_ke_typeqnode', 'claim_span_start', 'equivalent_claims', 'time_end_latest', 
#'x_end', 'claimer_start', 'end_char', 'refuting_claims', 'time_start_earliest', 'template', 
#'final_claim_score', 'claimer_ke_typeqnode', 'x_start', 'stance', 'x_ke', 'news_author', 
#'claim_semantics', 'topic_score', 'time_start_latest', 'claimer_ke_qnode', 'topic', 'claimer_text', 
#'segment_id', 'x_variable', 'claimer_score', 'claimer_qnode', 'qnode_x_variable_identity', 
#'qnode_x_variable_type', 'x_ke_qnode', 'claimer_type_qnode', 'sub_topic', 'supporting_claims', 
#'news_url', 'source', 'claimer_affiliation', 'claimer_affiliation_identity_qnode', 
#'claimer_affiliation_type_qnode', 'location', 'entity', 'lan', 'generation', 
#'time_attr', 'sentence_L', 'sentence_M', 'sentence_R', 'equivalent_claims_text', 
#'supporting_claims_text', 'refuting_claims_text', 'claimer_search_key', 'render_text']
#)

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
#          print(f"{image_path}{question}{answer}")
          claim = {"sentence":str(answer).strip(), \
                   "source":image_path, \
                   "claim_id":f"{len(claims):08}"}
          claims.append(claim)
        else:
          print(f"IGNORED line: {line}")

  with open(output_file, 'w') as f:
    container = {"claims":claims}
    json.dump(container, f, indent=2)

  print(f"Wrote: {output_file}\nDone.")

if __name__ == "__main__":
  main()
