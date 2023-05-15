# Getting started

## Random submission

```python
from pathlib import Path

import numpy as np

tasks = [
   (generator, epsilon)
   for generator in ["mst", "pategan", "privbayes"]
   for epsilon in [1, 10, 100, 1000]
]

n_targets = 100

rng = np.random.default_rng()

dirname = Path("my_random_submission")
dirname.mkdir()

for generator, epsilon in tasks:
   guess = rng.uniform(size=n_targets)
   
   fname = dirname / f"{generator}_{epsilon}.txt"
   
   np.savetxt(fname, guess, fmt="%f")
```

```shell
zip -j my_random_submission.zip my_random_submission/*.txt
```

## Synthesizers

We use [reprosyn](https://github.com/alan-turing-institute/reprosyn) to synthesize data. 

1. Create and activate the [provided environment](../envs/reprosyn.yaml):
    ```shell
    mamba env create -n snake1 -f ../envs/reprosyn.yaml
    conda activate snake1
    ```
2. You can call [`scripts.task_prep.create_task`](../scripts/task_prep.py) and [`scripts.task_synth.create_task_synth`](../scripts/task_synth.py) to create you own tasks.