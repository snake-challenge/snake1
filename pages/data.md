# Data

## Base

The data (available as `base.parquet`) is adapted from the [EPI CPS Basic Monthly](https://microdata.epi.org) dataset provided by the Economic Policy Institute.

We select a subset of attributes. Description is available at https://microdata.epi.org/variables/. 
The datatypes are encoded as ordered/unordered categorical when appropriate.
`meta.json` is a table schema in [TAPAS format](https://privacy-sdg-toolbox.readthedocs.io/en/latest/dataset-schema.html#json-format).
We consider the years 2005 to 2022. 
For each household (set of individuals), we keep only the month with the most records.
We drop all rows with missing values.

## Task files

Each task `generator`(ε=`epsilon`) is described by the following set of files:

### Public data

Available at `public_data_{phase}.zip`

- `{generator}_{epsilon}.sha512` contains a sha512 hash of public and private files; 
- `{generator}_{epsilon}_synthetic.csv` is the privacy-preserving synthetic data;
- `{generator}_{epsilon}_targets.csv` is the set of individual targets;
- `{generator}_{epsilon}_targets_index.txt` is the household index of targets.

### Private data

Private data will be published after the competition as `private_data_{phase}.zip`.

- `{generator}_{epsilon}_seed.json` RNG state use to sample train, targets and truth;
- `{generator}_{epsilon}_train.feather` data used to train the generator;
- `{generator}_{epsilon}.npy` membership truth.
