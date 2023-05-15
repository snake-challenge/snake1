import json

import pandas as pd
import numpy as np


def create_task(base, n_samples, n_targets, target_min_hh):
    rng = np.random.default_rng()
    state = rng.bit_generator.state

    hh_size = base.groupby("hhid").size()

    targets_mask = hh_size.ge(target_min_hh)
    targets_idx = targets_mask[targets_mask].index
    targets_idx = rng.choice(targets_idx, size=n_targets, replace=False)

    targets = base.loc[targets_idx]

    n_targets_pos = n_targets_neg = n_targets // 2
    truth = np.r_[np.ones(n_targets_pos, bool), np.zeros(n_targets_neg, bool)]
    rng.shuffle(truth)

    targets_idx_pos = targets_idx[truth]
    targets_pos = targets.loc[targets_idx_pos]

    n_train_comp = n_samples - len(targets)
    train_comp = base.drop(targets_idx).sample(n=n_train_comp, random_state=rng)
    train = pd.concat([targets_pos, train_comp]).sample(frac=1, random_state=rng)

    return state, targets_idx, targets, truth, train


def main():
    sm = snakemake  # noqa

    base = pd.read_parquet(sm.input[0])

    state, targets_idx, targets, truth, train = create_task(base, **sm.params)

    with open(sm.output.seed, "w") as f:
        json.dump(state, f)

    np.savetxt(sm.output.targets_idx, targets_idx, fmt="%d")
    targets.to_csv(sm.output.targets)

    np.savetxt(sm.output.truth, truth, fmt="%d")

    train.reset_index(drop=True).to_feather(sm.output.train)


if __name__ == "__main__":
    main()
