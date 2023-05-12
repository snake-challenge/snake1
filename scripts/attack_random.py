import numpy as np


sm = snakemake  # noqa

targets = np.loadtxt(sm.input[0])

rng = np.random.default_rng(123)

guess = rng.uniform(size=len(targets))

np.savetxt(sm.output[0], guess, fmt="%f")
