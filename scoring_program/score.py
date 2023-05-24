import argparse
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


parser = argparse.ArgumentParser()
parser.add_argument("--ref", type=Path)
parser.add_argument("--res-dir", type=Path)
parser.add_argument("--stdout", action="store_true")

args = parser.parse_args()

input_dir = Path("/app/input")
output_dir = Path("/app/output")

if args.ref is not None:
    ref = args.ref
else:
    ref_dir = input_dir / "ref"
    ref = next(ref_dir.iterdir())  # only one

assert ref.exists(), f"Missing reference file {ref}"

if args.res_dir is not None:
    res_dir = args.res_dir
else:
    res_dir = input_dir / "res"

res_name = f"{ref.stem}.txt"
res = res_dir / res_name
assert res.exists(), f"Missing submission file {res_name}"

truth = np.loadtxt(ref, dtype=float)
guess = np.loadtxt(res, dtype=float)

assert np.all((guess >= 0.0) & (guess <= 1.0)), "Submission outside of range [0, 1]"

assert truth.shape == guess.shape, f"Invalid number of lines: got {len(guess)} expected {len(truth)}"

weights = 2 * np.abs(0.5 - guess)
score = membership_advantage(truth, guess > 0.5, sample_weight=weights)

scores = {"ma": score}

print(f"Membership advantage = {score}")

if not args.stdout:
    with open(output_dir / "scores.json", "w") as f:
        json.dump(scores, f)
