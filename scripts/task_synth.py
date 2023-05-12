import json

import pandas as pd
import reprosyn.methods


def create_task_synth(train, metadata, generator, epsilon, n_samples):
    cls = getattr(reprosyn.methods, generator)
    gen = cls(
        dataset=train.reset_index(drop=True),
        metadata=metadata,
        size=n_samples,
        epsilon=epsilon,
    )
    gen.run()
    synth = gen.output.astype(train.dtypes)
    return synth


def main():
    sm = snakemake  # noqa

    with open(sm.input.meta) as f:
        metadata = json.load(f)

    train = pd.read_feather(sm.input.train)

    synth = create_task_synth(train, metadata, **sm.params)

    synth.to_csv(sm.output.synth, index=False)


if __name__ == "__main__":
    main()
