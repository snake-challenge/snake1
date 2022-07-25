from zipfile import ZipFile

import numpy as np
import pandas as pd


SEED = 2937224909

YEARS = range(2003, 2022)

DTYPES = {
    "year": "uint16",
    "month": "uint8",
    "hhid": "uint32",
    "hrhhid": "uint64",
    "age": "uint8",
    "agechild": "uint8",
    "citistat": "uint8",
    "female": "uint8",
    "married": "uint8",
    "ownchild": "uint8",
    "wbhaom": "uint8",
    "gradeatn": "uint8",
    "cow1": "uint8",
    "ftptstat": "uint8",
    "statefips": "uint8",
    "hoursut": "uint8",
    "faminc": "uint8",
    "mind16": "uint8",
    "mocc10": "uint8",
    "basicwgt": "float16",
}

sm = snakemake  # noqa

with ZipFile(sm.input[0]) as zf:

    def prepare1(year):
        # read from zip
        with zf.open(f"epi_cpsbasic_{year}.dta") as f:
            df1 = pd.read_stata(
                f,
                convert_categoricals=False,
                columns=list(DTYPES.keys()),
            )

        # restrict to age 16 and above and positive sample weight
        df1 = df1[df1.age.ge(16) & df1.basicwgt.gt(0)]

        # faminc missing values (before 2009)
        df1 = df1.replace({"faminc": {-3: np.nan, -2: np.nan, -1: np.nan}})
        # drop all rows with missing values
        df1 = df1.dropna()

        # best types
        df1 = df1.astype(DTYPES)
        # drop index (rows)
        df1 = df1.reset_index(drop=True)

        # drop sample weight
        df1 = df1.drop(columns=["basicwgt"])

        return df1

    # read and prepare all years
    dfs = map(prepare1, YEARS)
    # merge all years
    df = pd.concat(dfs, ignore_index=True, copy=False)

# sample one individual per household
df = (
    df.sample(frac=1, random_state=SEED)
    .groupby(["hhid", "hrhhid"], sort=False, as_index=True)
    .head(n=1)
    .drop(columns=["year", "month", "hhid", "hrhhid"])  # drop idx
)

# row as index (as column for feather)
df = df.rename_axis("row").reset_index()
df.to_feather(sm.output[0])
