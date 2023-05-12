# Getting Started

## Submission

Zip file containing `{generator}_{epsilon}.txt` for each task, with one guess ∈ [0, 1] per line for each *target household* (i.e., same number of lines as `{generator}_{epsilon}_targets_index.txt`).
We provide an example as `starting_kit_{phase}.zip`.

The total number of submissions is limited to 20, with at most 2 submissions per day. You can however generate you own tasks locally to evaluate your attack.

## Environment

You can use [`envs/reprosyn.yaml`](https://github.com/snake-challenge/snake1/blob/Main/envs/reprosyn.yaml) to create a Conda environment with all the packages used to create tasks (and synthesize data). 
See https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#creating-an-environment-from-an-environment-yml-file.

## File formats

We use different file formats, all readable with either Pandas or Numpy (and many other libraries).

- [`.parquet`](https://parquet.apache.org/) readable with [`pandas.read_parquet`](https://pandas.pydata.org/docs/reference/api/pandas.read_parquet.html)
- [`.feather`](https://arrow.apache.org/docs/python/feather.html) readable with [`pandas.read_feather`](https://pandas.pydata.org/docs/reference/api/pandas.read_feather.html)
- pickled numpy `.npy` readable with [`numpy.load`](https://numpy.org/doc/stable/reference/generated/numpy.load.html) (reference data)
- comma-separated values `.csv` readable with [`pandas.read_csv`](https://pandas.pydata.org/docs/reference/api/pandas.read_csv.html)
- submissions as `.txt` (see above) writable with [`numpy.savetxt`](https://numpy.org/doc/stable/reference/generated/numpy.savetxt.html) with `fmt="%f"`.

## Example

A random submission can be created as follow:

```python
import numpy as np

n_targets = 100
generator = "mst"
epsilon = 1

rng = np.random.default_rng(123)

guess = rng.uniform(size=n_targets)

np.savetxt(f"{generator}_{epsilon}.txt", guess, fmt="%f")
```