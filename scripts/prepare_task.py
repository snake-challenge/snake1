import numpy as np
import pandas as pd

sm = snakemake  # noqa

seed = sm.params.seed
n_samples = sm.params.n_samples
n_targets = sm.params.n_targets
bg_ratio = sm.params.task["background"]

rng = np.random.default_rng(seed)

data = pd.read_feather(sm.input[0]).set_index("row")

train = data.sample(n=n_samples, random_state=rng)
train.to_csv(sm.output.train, index=False)  # no index

background = train.sample(frac=bg_ratio, random_state=rng)
background.to_csv(sm.output.background)

t = data.drop(background.index)  # targets are not in background
a = t.index.isin(train.index)
wgts = np.where(a, 1 / np.sum(a), 1 / np.sum(~a))  # balance train/~train
targets = t.sample(n=n_targets, weights=wgts, random_state=rng)
targets.to_csv(sm.output.targets)

truth = targets.index.isin(train.index)
np.savetxt(sm.output.truth, truth, fmt="%i")
