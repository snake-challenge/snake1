import json
from pathlib import Path

import numpy as np
from sklearn.metrics import confusion_matrix


def membership_advantage(y_true, y_pred, sample_weight):
    cm = confusion_matrix(y_true, y_pred, sample_weight=sample_weight)
    tn, fp, fn, tp = cm.ravel()
    tpr = tp / (tp + fn)
    fpr = fp / (tn + fp)
    ma = tpr - fpr
    ma = (ma + 1) / 2
    return ma


input_dir = Path("/app/input")
output_dir = Path("/app/output")

ref_dir = input_dir / "ref"
ref = next(ref_dir.iterdir())  # only one
assert ref.exists()

res_name = f"{ref.stem}.txt"
res = input_dir / "res" / res_name
assert res.exists()

truth = np.loadtxt(ref, dtype=float)
guess = np.loadtxt(res, dtype=float)

assert truth.shape == guess.shape

weights = 2 * np.abs(0.5 - guess)
score = membership_advantage(truth, guess > 0.5, sample_weight=weights)

scores = {"ma": score}

with open(output_dir / "scores.json", "w") as f:
    json.dump(scores, f)
