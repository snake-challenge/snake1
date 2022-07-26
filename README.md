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

## Optimization

1. Create optimization environment

```
$ mamba env create -f envs/synthesizers.yaml -n opt
$ conda activate opt
(opt) $ conda env config vars set LD_LIBRARY_PATH=$CONDA_PREFIX/lib
(opt) $ pip install guildai 
(opt) $ conda deactivate
$ conda activate opt 
```

2. Run trials

```
(opt) $ guild run privbayes:train --maximize BNLogLikelihood histogram_bins=[10:20] degree=[1:10]
```

Refer to [guild.yml]() for parameters

3. You can view runs (in real-time) with

```
(opt) $ guild view
```