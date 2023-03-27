from vizwiz_api.vizwiz import VizWiz
from vizwiz_eval_cap.eval import VizWizEvalCap
import matplotlib.pyplot as plt
import numpy as np
import sys
import json
from json import encoder
encoder.FLOAT_REPR = lambda o: format(o, '.3f')
annFile = sys.argv[1]
resFile = sys.argv[2]
print(f"annFile: {annFile}\tresFile: {resFile}")
try:
  vizwiz = VizWiz(annFile, ignore_rejected=True, ignore_precanned=True)
  vizwizRes = vizwiz.loadRes(resFile)
  vizwizEval = VizWizEvalCap(vizwiz, vizwizRes)
  vizwizEval.evaluate()
  for metric, score in vizwizEval.eval.items():
    print('%s: %.3f'%(metric, score))
except KeyError:
  print('No annotations found to do scoring.')
