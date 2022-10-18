from functools import cached_property
from pathlib import Path

import click
import numpy as np
import pandas as pd

from snake1.synthesizers.base import Synthesizer

SYNTHESIZERS = ["CopulaShirley", "MST", "PateGan", "PrivBayes"]

N_SAMPLES = 10000

N_TARGETS = 100

INDEX_COL = "row"

PositiveFloat = click.FloatRange(min=0, min_open=True)
PositiveInt = click.IntRange(min=1)
UnitOpenRight = click.FloatRange(min=0, max=1, max_open=True)


class Task:
    def __init__(
        self,
        data: pd.DataFrame,
        synthesizer: str,
        epsilon: float,
        background_frac: float,
        seed: int = None,
        n_samples: int = N_SAMPLES,
        n_targets: int = N_TARGETS,
    ):
        self.synthesizer = synthesizer
        self.epsilon = epsilon
        self.background_frac = background_frac
        self.n_samples = n_samples
        self.n_targets = n_targets

        self.data = data

        self.seed = seed
        ss = np.random.SeedSequence(seed)
        self.seed_train, self.seed_background, self.seed_targets = ss.generate_state(3)

    @cached_property
    def train(self):
        return self.data.sample(
            n=self.n_samples, replace=False, random_state=self.seed_train
        )

    @cached_property
    def background(self):
        return self.train.sample(
            frac=self.background_frac, replace=False, random_state=self.seed_background
        )

    @cached_property
    def targets(self):
        data_wo_bg = self.data.drop(self.background.index)
        mask = data_wo_bg.index.isin(self.train.index)
        w = np.where(mask, *np.bincount(mask, minlength=2))
        targets = data_wo_bg.sample(
            n=self.n_targets, weights=w, replace=False, random_state=self.seed_targets
        )
        return targets

    @cached_property
    def truth(self):
        return self.targets.assign(truth=self.targets.index.isin(self.train.index))

    @cached_property
    def synthetic(self):
        # TODO: seed?
        synthesizer_cls = Synthesizer.by_name(self.synthesizer)
        synthesizer = synthesizer_cls(epsilon=self.epsilon)
        return synthesizer.fit_sample(self.train)

    def save(self, dest_dir: str):
        dest_dir = Path(dest_dir)
        dest_dir.mkdir(parents=True, exist_ok=True)

        self.train.to_csv(dest_dir / "train.csv", index=False)
        self.background.to_csv(dest_dir / "background.csv")
        self.targets.to_csv(dest_dir / "targets.csv")
        self.truth.to_csv(dest_dir / "truth.csv")
        self.synthetic.to_csv(dest_dir / "synth.csv", index=False)

    @staticmethod
    @click.command("task")
    @click.argument("data_path", type=click.Path(exists=True))
    @click.argument("dest_dir", type=click.Path(file_okay=False, writable=True))
    @click.option(
        "--synthesizer",
        type=click.Choice(SYNTHESIZERS, case_sensitive=False),
        required=True,
    )
    @click.option("--epsilon", type=PositiveFloat, required=True)
    @click.option("--background-frac", type=UnitOpenRight, required=True)
    @click.option("--seed", type=int, default=None)
    @click.option("--n-samples", type=PositiveInt, default=N_SAMPLES, show_default=True)
    @click.option("--n-targets", type=PositiveInt, default=N_TARGETS, show_default=True)
    def cli(
        data_path,
        dest_dir,
        synthesizer,
        epsilon,
        background_frac,
        seed,
        n_samples,
        n_targets,
    ):
        data = pd.read_feather(data_path).set_index(INDEX_COL)
        task = Task(
            data=data,
            synthesizer=synthesizer,
            epsilon=epsilon,
            background_frac=background_frac,
            seed=seed,
            n_samples=n_samples,
            n_targets=n_targets,
        )
        task.save(dest_dir)


if __name__ == "__main__":
    Task.cli()
