import json

import click
import numpy as np
import pandas as pd

INDEX_COL = "row"

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

ORD_COLUMNS = ["gradeatn", "faminc"]


@click.group(name="meta")
def cli():
    pass


@cli.command()
@click.argument("data_path", type=click.Path(exists=True))
def domain(data_path):
    data = pd.read_feather(data_path).set_index(INDEX_COL)
    dom = data.max().add(1).to_dict()
    click.echo(json.dumps(dom))


@cli.command()
@click.argument("data_path", type=click.Path(exists=True))
def metadata(data_path):
    data = pd.read_feather(data_path).set_index(INDEX_COL)
    meta = {
        "columns": [
            {"name": col}
            | (
                {
                    "type": ("Ordinal" if col in ORD_COLUMNS else "Categorical"),
                    "size": int(np.ptp(s)),
                    "i2s": s.drop_duplicates().sort_values().tolist(),
                }
                if col in CAT_COLUMNS
                else {"type": "Integer", "min": int(s.min()), "max": int(s.max())}
            )
            for col, s in data.items()
        ]
    }
    click.echo(json.dumps(meta))


if __name__ == "__main__":
    cli()
