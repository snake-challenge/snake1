import argparse
import json
from pathlib import Path
from pydoc import locate  # import obj by name

import pandas as pd

parser = argparse.ArgumentParser()

ALGOS = {
    "copulashirley": "synthesizers.copulashirley.MyCopulaShirley",
    "mst": "synthesizers.mst.MyMST",
    "pategan": "synthesizers.pategan.MyPATEGAN",
    "privbayes": "synthesizers.privbayes.MyPrivBayes",
}

parser.add_argument("input", type=Path)
parser.add_argument("output", type=Path)
parser.add_argument("algorithm", choices=ALGOS.keys())
parser.add_argument("n_samples", type=int)
parser.add_argument("epsilon", type=float)

parser.add_argument("opt", type=str)

args = parser.parse_args()

MyModel = locate(ALGOS[args.algorithm])

opt = json.loads(args.opt)

train_df = pd.read_csv(args.input)

g = MyModel(epsilon=args.epsilon, **opt)
g.fit(train_df)

synth_df = g.generate_samples(args.n_samples)
synth_df.to_csv(args.output, index=False)
