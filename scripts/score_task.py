import numpy as np
import pandas as pd

sm = snakemake  # noqa

attack = np.loadtxt(sm.input.attack, dtype=bool)
truth = np.loadtxt(sm.input.truth, dtype=bool)

cm = (
    pd.crosstab(truth, attack)
    # TODO: reindex fill_value?
    .reindex([False, True]).reindex([False, True], axis=1)
)

tn, fp, fn, tp = cm.to_numpy().ravel()

tpr = tp / (tp + fn)
fpr = fp / (tn + fp)
ma = tpr - fpr

task = dict(sm.params["task"])
task["membership_advantage"] = ma

scores = pd.DataFrame([task])
scores.to_csv(sm.output[0], index=False)
