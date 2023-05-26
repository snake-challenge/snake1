# Getting Started

The data is available as release artifacts at https://github.com/snake-challenge/snake1/

## Public data

Task inputs are available as `public_data_{phase}.zip`. *See the Data tab for details about this dataset*.

## Submission

One submission should take the form of a Zip file containing a file called `{generator}_{epsilon}.txt` for each task, with one guess ∈ [0, 1] per line for each *target household* (*i.e.*, the number of lines should be the same as `{generator}_{epsilon}_targets_index.txt`).
We provide an example of a dummy submission file in `starting_kit_{phase}.zip`.

Note that the zip file (submission file) needs to contain the *results of the attacks for all tasks*.
In addition, the score of a user will be computed on a single submission chosen and explicitely validated by the user and not on the best one for each task (*i.e.*, this means that the leaderboard will not remember the previous scores of each task but only display the ones related to the chosen submission).
In practice, this means that you need to add explicitely your chosen submission to the leaderboard for it to be taken into account.

**Limit of the number of submissions**: The total number of submissions per participant is limited to 20, with at most 2 submissions per day.
To experiment without the submission limit, you can use the [*playground challenge*](https://www.codabench.org/competitions/880/) which uses different data and allows any number of submissions. 

## Environment

You can use [`envs/reprosyn.yaml`](https://github.com/snake-challenge/snake1/blob/Main/envs/reprosyn.yaml) to create a Conda environment with all the packages used to create the tasks and synthesized data:

```commandline
$ conda env create -n snake1 -f reprosyn.yaml
```

See https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#creating-an-environment-from-an-environment-yml-file.

## File formats

We use different file formats, all readable with either Pandas or Numpy (as well as many other libraries).

- [`.parquet`](https://parquet.apache.org/) readable with [`pandas.read_parquet`](https://pandas.pydata.org/docs/reference/api/pandas.read_parquet.html)
- [`.feather`](https://arrow.apache.org/docs/python/feather.html) readable with [`pandas.read_feather`](https://pandas.pydata.org/docs/reference/api/pandas.read_feather.html)
- comma-separated values `.csv` readable with [`pandas.read_csv`](https://pandas.pydata.org/docs/reference/api/pandas.read_csv.html)
- submissions as `.txt` (see above) writable with [`numpy.savetxt`](https://numpy.org/doc/stable/reference/generated/numpy.savetxt.html) with `fmt="%f"`.

## Example of generation of a random submission

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