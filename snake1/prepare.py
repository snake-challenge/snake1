import click
import pandas as pd
from joblib import Parallel, delayed

INDEX_COL = "row"

COLUMNS = [
    "hhid",
    "hrhhid",
    "age",
    "agechild",
    "citistat",
    "female",
    "married",
    "ownchild",
    "wbhaom",
    "gradeatn",
    "cow1",
    "ftptstat",
    "statefips",
    "hoursut",
    "faminc",
    "mind16",
    "mocc10",
    "basicwgt",
]

CAT_COLUMNS = [
    "agechild",
    "citistat",
    "female",
    "married",
    "wbhaom",
    "cow1",
    "ftptstat",
    "statefips",
    "mind16",
    "mocc10",
    "gradeatn",
    "faminc",
]

DATA_DTYPE = "uint8"


@click.command()
@click.argument("input_paths", type=click.Path(), nargs=-1)
@click.argument("data_path", type=click.Path(writable=True))
@click.option("--n-jobs", type=int)
@click.option("--seed", type=int)
def prepare(input_paths, data_path, n_jobs=None, seed=None):
    def prep(fn):
        return (
            pd.read_feather(fn, columns=COLUMNS)
            .dropna()
            .query("faminc >= 0 & age >= 16 & basicwgt > 0")
            .drop("basicwgt", axis=1)
        )

    dfs = Parallel(n_jobs=n_jobs)(delayed(prep)(fn) for fn in input_paths)

    df = pd.concat(dfs, ignore_index=True, copy=False)

    # normalize categorical features to [0, n-1] with continuous values
    df[CAT_COLUMNS] = pd.concat(
        Parallel(n_jobs=n_jobs, batch_size=2)(
            delayed(lambda s: s.astype("category").cat.codes)(df[c])
            for c in CAT_COLUMNS
        ),
        axis=1,
    )

    df = df.astype(DATA_DTYPE)

    df = df - df.min()  # normalize all to [0, n-1]

    # sample one individual per household
    df = (
        df.sample(frac=1, random_state=seed)
        .groupby(["hhid", "hrhhid"], sort=False)
        .head(n=1)
        .drop(columns=["hhid", "hrhhid"])
        .rename_axis(INDEX_COL)
        .reset_index()
    )

    df.to_feather(data_path)


if __name__ == "__main__":
    prepare()
