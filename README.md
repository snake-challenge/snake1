# SNAKE SaNitization Algorithm under attacK ...ε

## Setup

1. Install [Mamba](https://github.com/mamba-org/mamba)

2. Create environment

```
$ mamba create -n snake1 -c conda-forge -c bioconda -c snakemake pyarrow
```

## Usage

1. Activate environment

```
$ conda activate snake1
```

2. Run target

```
(snake1) $ snakemake --cores all --use-conda <target>
```

### Examples

1. Create and eval *one task*

- [ ] TODO: shortcut?

```
(snake1) $ snakemake --cores all --use-conda results/team~<NAME>/algorithm~<ALGORITHM>/epsilon~<EPSILON>/background~<BACKGROUND>/synth.csv
(snake1) $ snakemake --cores all --use-conda results/team~<NAME>/algorithm~<ALGORITHM>/epsilon~<EPSILON>/background~<BACKGROUND>/score.csv
```

3. Create and eval *all tasks of a team*

- [ ] TODO: shortcut

4. Using the attack environment

- [ ] TODO: shortcut
- [ ] TODO: demo script

5. Adding an *attack result*

Write to `results/team~<NAME>/algorithm~<ALGORITHM>/epsilon~<EPSILON>/background~<BACKGROUND>/attack.csv`

- [ ] TODO: check overwrite

6. Registering an *attack script* into the workflow 

- [ ] TODO