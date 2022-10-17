import click
import numpy as np
import pandas as pd


def membership_advantage(y_true, y_pred):
    cm = (
        pd.crosstab(y_true, y_pred)
        .reindex([False, True])
        .reindex([False, True], axis=1)
    )
    tn, fp, fn, tp = cm.to_numpy().ravel()

    tpr = tp / (tp + fn)
    fpr = fp / (tn + fp)

    ma = tpr - fpr

    return ma


@click.command()
@click.argument("truth_path", type=click.Path(exists=True))
@click.argument("attack_path", type=click.Path(exists=True))
def score(truth_path, attack_path):
    truth = pd.read_csv(truth_path)

    attack = np.loadtxt(attack_path, dtype=bool)

    # assert len(truth) == len(attack)

    truth["attack"] = attack

    ma = membership_advantage(truth.truth, truth.attack)

    click.echo(ma)


if __name__ == "__main__":
    score()
