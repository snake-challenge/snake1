import click
import pandas as pd
from sdmetrics.single_table import (
    BNLogLikelihood,
    LogisticDetection,
    GMLogLikelihood,
    CSTest,
    ContinuousKLDivergence,
    DiscreteKLDivergence,
)

METADATA = {
    "fields": {
        "age": {"type": "numerical"},
        "agechild": {"type": "categorical"},
        "citistat": {"type": "categorical"},
        "female": {"type": "categorical"},
        "married": {"type": "categorical"},
        "ownchild": {"type": "numerical"},
        "wbhaom": {"type": "categorical"},
        "gradeatn": {"type": "Ordinal"},
        "cow1": {"type": "categorical"},
        "ftptstat": {"type": "categorical"},
        "statefips": {"type": "categorical"},
        "hoursut": {"type": "numerical"},
        "faminc": {"type": "Ordinal"},
        "mind16": {"type": "categorical"},
        "mocc10": {"type": "categorical"},
    }
}


@click.command()
@click.argument("train_path", type=click.Path(exists=True))
@click.argument("synth_path", type=click.Path(exists=True))
def util(train_path, synth_path):
    metrics = [
        BNLogLikelihood(),
        LogisticDetection(),
        GMLogLikelihood(),
        CSTest,
        ContinuousKLDivergence(column_pairs_metric=ContinuousKLDivergence),
        DiscreteKLDivergence(column_pairs_metric=ContinuousKLDivergence),
    ]

    train = pd.read_csv(train_path)
    synth = pd.read_csv(synth_path)

    res = {
        metric.__class__.__name__: metric.compute(
            train, synth, metadata=METADATA
        )
        for metric in metrics
    }

    click.echo(res)


if __name__ == "__main__":
    util()
