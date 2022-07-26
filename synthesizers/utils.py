import pandas as pd

CPSBASIC_PATH = "results/cpsbasic.feather"

METADATA_SYNTHETIC_DATA_RELEASE = {
    "columns": [
        {"name": "age", "type": "Integer", "min": 16, "max": 80},
        {"name": "ownchild", "type": "Integer", "min": 0, "max": 13},
        {"name": "hoursut", "type": "Integer", "min": 0, "max": 198},
        {
            "name": "agechild",
            "type": "Categorical",
            "size": 16,
            "i2s": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
        },
        {
            "name": "citistat",
            "type": "Categorical",
            "size": 5,
            "i2s": [1, 2, 3, 4, 5],
        },
        {"name": "female", "type": "Categorical", "size": 2, "i2s": [0, 1]},
        {"name": "married", "type": "Categorical", "size": 2, "i2s": [0, 1]},
        {
            "name": "wbhaom",
            "type": "Categorical",
            "size": 6,
            "i2s": [1, 2, 3, 4, 5, 6],
        },
        {
            "name": "cow1",
            "type": "Categorical",
            "size": 8,
            "i2s": [1, 2, 3, 4, 5, 6, 7, 8],
        },
        {
            "name": "ftptstat",
            "type": "Categorical",
            "size": 9,
            "i2s": [2, 3, 4, 5, 6, 7, 8, 9, 10],
        },
        {
            "name": "statefips",
            "type": "Categorical",
            "size": 51,
            "i2s": [
                1,
                2,
                4,
                5,
                6,
                8,
                9,
                10,
                11,
                12,
                13,
                15,
                16,
                17,
                18,
                19,
                20,
                21,
                22,
                23,
                24,
                25,
                26,
                27,
                28,
                29,
                30,
                31,
                32,
                33,
                34,
                35,
                36,
                37,
                38,
                39,
                40,
                41,
                42,
                44,
                45,
                46,
                47,
                48,
                49,
                50,
                51,
                53,
                54,
                55,
                56,
            ],
        },
        {
            "name": "mind16",
            "type": "Categorical",
            "size": 16,
            "i2s": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
        },
        {
            "name": "mocc10",
            "type": "Categorical",
            "size": 10,
            "i2s": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        },
        {
            "name": "gradeatn",
            "type": "Ordinal",
            "size": 16,
            "i2s": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
        },
        {
            "name": "faminc",
            "type": "Ordinal",
            "size": 15,
            "i2s": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
        },
    ]
}


DOMAIN = {
    "age": 65,
    "agechild": 16,
    "citistat": 5,
    "female": 2,
    "married": 2,
    "ownchild": 14,
    "wbhaom": 6,
    "gradeatn": 16,
    "cow1": 8,
    "ftptstat": 9,
    "statefips": 56,
    "hoursut": 199,
    "faminc": 15,
    "mind16": 16,
    "mocc10": 10,
}

MIN_VALS = {
    "age": 16,
    "agechild": 0,
    "citistat": 1,
    "female": 0,
    "married": 0,
    "ownchild": 0,
    "wbhaom": 1,
    "gradeatn": 1,
    "cow1": 1,
    "ftptstat": 2,
    "statefips": 1,
    "hoursut": 0,
    "faminc": 1,
    "mind16": 1,
    "mocc10": 1,
}

CAT_COLS = [
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

METADATA_SDMETRICS = {
    "fields": {
        "age": {
            "name": "age",
            "type": "numerical",
            "subtype": "integer",
            "min": 16,
            "max": 80,
        },
        "ownchild": {
            "name": "ownchild",
            "type": "numerical",
            "subtype": "integer",
            "min": 0,
            "max": 13,
        },
        "hoursut": {
            "name": "hoursut",
            "type": "numerical",
            "subtype": "integer",
            "min": 0,
            "max": 198,
        },
        "agechild": {
            "name": "agechild",
            "type": "categorical",
            "size": 16,
            "i2s": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
        },
        "citistat": {
            "name": "citistat",
            "type": "categorical",
            "size": 5,
            "i2s": [1, 2, 3, 4, 5],
        },
        "female": {"name": "female", "type": "categorical", "size": 2, "i2s": [0, 1]},
        "married": {"name": "married", "type": "categorical", "size": 2, "i2s": [0, 1]},
        "wbhaom": {
            "name": "wbhaom",
            "type": "categorical",
            "size": 6,
            "i2s": [1, 2, 3, 4, 5, 6],
        },
        "cow1": {
            "name": "cow1",
            "type": "categorical",
            "size": 8,
            "i2s": [1, 2, 3, 4, 5, 6, 7, 8],
        },
        "ftptstat": {
            "name": "ftptstat",
            "type": "categorical",
            "size": 9,
            "i2s": [2, 3, 4, 5, 6, 7, 8, 9, 10],
        },
        "statefips": {
            "name": "statefips",
            "type": "categorical",
            "size": 51,
            "i2s": [
                1,
                2,
                4,
                5,
                6,
                8,
                9,
                10,
                11,
                12,
                13,
                15,
                16,
                17,
                18,
                19,
                20,
                21,
                22,
                23,
                24,
                25,
                26,
                27,
                28,
                29,
                30,
                31,
                32,
                33,
                34,
                35,
                36,
                37,
                38,
                39,
                40,
                41,
                42,
                44,
                45,
                46,
                47,
                48,
                49,
                50,
                51,
                53,
                54,
                55,
                56,
            ],
        },
        "mind16": {
            "name": "mind16",
            "type": "categorical",
            "size": 16,
            "i2s": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
        },
        "mocc10": {
            "name": "mocc10",
            "type": "categorical",
            "size": 10,
            "i2s": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        },
        "gradeatn": {
            "name": "gradeatn",
            "type": "numerical",
            "subtype": "integer",
            "size": 16,
            "i2s": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
        },
        "faminc": {
            "name": "faminc",
            "type": "numerical",
            "subtype": "integer",
            "size": 15,
            "i2s": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
        },
    },
    "target": "female",  # TODO: param?
}


def score(train, synth):
    from sdmetrics.single_table import (
        BNLogLikelihood,
        LogisticDetection,
        SVCDetection,
        BinaryDecisionTreeClassifier,
        BinaryAdaBoostClassifier,
        BinaryLogisticRegression,
        BinaryMLPClassifier,
        MulticlassDecisionTreeClassifier,
        MulticlassMLPClassifier,
        LinearRegression,
        MLPRegressor,
        GMLogLikelihood,
        CSTest,
        KSTest,
        KSTestExtended,
        ContinuousKLDivergence,
        DiscreteKLDivergence,
    )

    metrics = [
        BNLogLikelihood(),
        LogisticDetection(),
        SVCDetection(),
        BinaryDecisionTreeClassifier(),
        BinaryAdaBoostClassifier(),
        BinaryLogisticRegression(),
        BinaryMLPClassifier(),
        MulticlassDecisionTreeClassifier(),
        MulticlassMLPClassifier(),
        LinearRegression(),
        MLPRegressor(),
        GMLogLikelihood(),
        CSTest,
        KSTest,
        KSTestExtended,
        ContinuousKLDivergence(column_pairs_metric=ContinuousKLDivergence),
        DiscreteKLDivergence(column_pairs_metric=ContinuousKLDivergence),
    ]

    return {
        metric.__class__.__name__: metric.compute(
            train, synth, metadata=METADATA_SDMETRICS
        )
        for metric in metrics
    }


def train_gen_score(n_samples, model):
    train = (
        pd.read_feather(CPSBASIC_PATH)
        .drop(columns=["row"])  # drop index
        .sample(n=n_samples)
        .astype(int)  # sdmetrics does not like uint
    )

    model.fit(train)
    synth = model.generate_samples(n_samples).astype(train.dtypes)

    return score(train, synth)
