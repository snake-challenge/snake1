import json
from zipfile import ZipFile

import pandas as pd

columns = [
    "year",
    "month",
    "hhid",
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

labels = {
    "agechild": {
        0: "No own children under 18 years of age",
        1: "All own children 0-2 years of age",
        2: "All own children 3-5 years of age",
        3: "All own children 6-13 years of age",
        4: "All own children 14-17 years of age",
        5: "Own children 0-2 and 3-5 years of age (none 6-17)",
        6: "Own children 0-2 and 6-13 years of age (none 3-5 or 14-17)",
        7: "Own children 0-2 and 14-17 years of age (none 3-13)",
        8: "Own children 3-5 and 6-13 years of age (none 0-2 or 14-17)",
        9: "Own children 3-5 and 14-17 years of age (none 0-2 or 6-13)",
        10: "Own children 6-13 and 14-17 years of age (none 0-5)",
        11: "Own children 0-2, 3-5, and 6-13 years of age (none 14-17)",
        12: "Own children 0-2, 3-5, and 14-17 years of age (none 6-13)",
        13: "Own children 0-2, 6-13, and 14-17 years of age (none 3-5)",
        14: "Own children 3-5, 6-13, and 14-17 years of age (none 0-2)",
        15: "Own children from all age groups",
    },
    "citistat": {
        1: "Native, born in US",
        2: "Native, born in Puerto Rico or other US island areas",
        3: "Native, born abroad with American parent(s)",
        4: "Foreign born, naturalized US citizen",
        5: "Foreign born, not a US citizen",
    },
    "female": {0: "Male", 1: "Female"},
    "married": {0: "Not married", 1: "Married"},
    "wbhaom": {
        1: "White",
        2: "Black",
        3: "Hispanic",
        4: "Asian",
        5: "Native American",
        6: "Multiple races",
    },
    "gradeatn": {
        1: "Less than 1st grade",
        2: "1st-4th grade",
        3: "5th-6th grade",
        4: "7th-8th grade",
        5: "9th grade",
        6: "10th grade",
        7: "11th grade",
        8: "12th grade-no diploma",
        9: "HS graduate, GED",
        10: "Some college but no degree",
        11: "Associate degree-occupational/vocational",
        12: "Associate degree-academic program",
        13: "Bachelor's degree",
        14: "Master's degree",
        15: "Professional school",
        16: "Doctorate",
    },
    "cow1": {
        1: "Government - Federal",
        2: "Government - State",
        3: "Government - Local",
        4: "Private, for profit",
        5: "Private, nonprofit",
        6: "Self-employed, incorporated",
        7: "Self-employed, unincorporated",
        8: "Without pay",
    },
    "ftptstat": {
        1: "Not in labor force",
        2: "FT hours (35+), usually FT",
        3: "PT for economic reasons, usually FT",
        4: "PT for non-economic reasons, usually FT",
        5: "Not at work, usually FT",
        6: "PT hrs, usually PT for economic reasons",
        7: "PT hrs, usually PT for non-economic reasons",
        8: "FT hours, usually PT for economic reasons",
        9: "FT hours, usually PT for non-economic",
        10: "Not at work, usually part-time",
        11: "Unemployed FT",
        12: "Unemployed PT",
    },
    "statefips": {
        1: "AL",
        2: "AK",
        4: "AZ",
        5: "AR",
        6: "CA",
        8: "CO",
        9: "CT",
        10: "DE",
        11: "DC",
        12: "FL",
        13: "GA",
        15: "HI",
        16: "ID",
        17: "IL",
        18: "IN",
        19: "IA",
        20: "KS",
        21: "KY",
        22: "LA",
        23: "ME",
        24: "MD",
        25: "MA",
        26: "MI",
        27: "MN",
        28: "MS",
        29: "MO",
        30: "MT",
        31: "NE",
        32: "NV",
        33: "NH",
        34: "NJ",
        35: "NM",
        36: "NY",
        37: "NC",
        38: "ND",
        39: "OH",
        40: "OK",
        41: "OR",
        42: "PA",
        44: "RI",
        45: "SC",
        46: "SD",
        47: "TN",
        48: "TX",
        49: "UT",
        50: "VT",
        51: "VA",
        53: "WA",
        54: "WV",
        55: "WI",
        56: "WY",
    },
    "faminc": {
        1: "Less than $5,000",
        2: "$5,000 - $7,499",
        3: "$7,500 - $9,999",
        4: "$10,000 - $12,499",
        5: "$12,500 - $14,999",
        6: "$15,000 - $19,999",
        7: "$20,000 - $24,999",
        8: "$25,000 - $29,999",
        9: "$30,000 - $34,999",
        10: "$35,000 - $39,999",
        11: "$40,000 - $49,999",
        12: "$50,000 - $74,999",
        13: "$75,000 - $99,999",
        14: "$100,000 - $149,999",
        15: "$150,000+",
    },
    "mind16": {
        1: "Agriculture, mining, forestry and fisheries",
        2: "Construction",
        3: "Manufacturing, durable goods",
        4: "Manufacturing, nondurable goods",
        5: "Transportation",
        6: "Communications and utilities",
        7: "Wholesale trade",
        8: "Retail trade",
        9: "Finance, insurance and real estate. Business, auto, repair, and other professional services.",
        10: "Personal services, including private household",
        11: "Entertainment and recreation",
        12: "Hospital",
        13: "Medical, except hospital",
        14: "Educational",
        15: "Social Services",
        16: "Public administration",
    },
    "mocc10": {
        1: "Managers and professionals",
        2: "Technicians",
        3: "Sales",
        4: "Office and admin",
        5: "Personal care and personal services",
        6: "Protective service",
        7: "Services",
        8: "Precision production, craft and repair",
        9: "Operators, fabricators and laborers",
        10: "Agriculture",
    },
}

ordered = {
    "age": True,
    "agechild": False,
    "citistat": False,
    "female": False,
    "married": False,
    "ownchild": True,
    "wbhaom": False,
    "gradeatn": True,
    "cow1": False,
    "ftptstat": False,
    "statefips": False,
    "hoursut": True,
    "faminc": True,
    "mind16": False,
    "mocc10": False,
}

dtypes = {
    c: pd.CategoricalDtype(l.values(), ordered=ordered[c]) for c, l in labels.items()
}

years = range(2005, 2023)


def prepare_data(zip_path, chunksize):
    dfs = []

    with ZipFile(zip_path) as zip_ref:

        for year in years:

            with zip_ref.open(f"epi_cpsbasic_{year}.dta") as dta_file:

                with pd.read_stata(
                    dta_file,
                    convert_categoricals=False,
                    preserve_dtypes=False,
                    columns=columns,
                    chunksize=chunksize,
                ) as itr:
                    for chunk in itr:
                        df = (
                            chunk.dropna()
                            .astype(int)
                            .query("faminc > 0 & age >= 16 & basicwgt > 0")
                            .drop("basicwgt", axis=1)
                            .replace(labels)
                            .astype(dtypes)
                        )
                        dfs.append(df)

    df = pd.concat(dfs, ignore_index=True, copy=False).set_index(
        ["hhid", "year", "month"]
    )
    return df


def select_households(df):
    hh_size = df.groupby(["hhid", "year", "month"]).size().sort_values(ascending=False)

    mask_hh = hh_size.index.get_level_values("hhid").duplicated(keep="first")
    hh_idx = hh_size.index[~mask_hh]

    hh = df.loc[hh_idx].droplevel(["year", "month"]).sort_index()

    return hh


def get_metadata_reprosyn(df):
    metadata = [
        {
            "name": label,
            "type": (
                "finite/ordered"
                if (not s.dtype == "category") or s.cat.ordered
                else "finite"
            ),
            "representation": (
                s.cat.categories.tolist()
                if s.dtype == "category"
                else list(map(str, range(s.min(), s.max() + 1)))
            ),
        }
        for label, s in df.items()
    ]

    return metadata


def main():
    sm = snakemake  # noqa

    df = prepare_data(sm.input[0], **sm.params)

    metadata = get_metadata_reprosyn(df)

    hh = select_households(df)

    with open(sm.output.meta, "w") as f:
        json.dump(metadata, f)

    hh.to_parquet(sm.output.data)


if __name__ == "__main__":
    main()
