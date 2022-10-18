# SNAKE1

wip tech report

## Data

### Source

[EPI CPS Basic monthly extracts](https://microdata.epi.org) from years 2003 to 2021.

### Variables
                                 
see https://microdata.epi.org/variables/

| Feature   | Type | Domain   | Description                           |
|-----------|------|----------|---------------------------------------|
| age       | int  | [0, 64]  |                                       |
| agechild  | cat  | [0, 15]  | number of own children by age group   |
| citistat  | cat  | [0, 4]   | native and citizenship                |
| female    | cat  | [0, 1]   |                                       |
| married   | cat  | [0, 1]   |                                       |
| ownchild  | int  | [0, 11]  | number of own children                |
| wbhaom    | cat  | [0, 5]   | race or ethnicity of the individual   |
| gradeatn  | ord  | [0, 15]  | education level attained              |
| cow1      | cat  | [0, 7]   | class of work for the primary job     |
| ftptstat  | cat  | [0, 8]   | full/part-time work status            |
| statefips | cat  | [0, 50]  | state of residence                    |
| hoursut   | int  | [0, 198] | usual hours worked per week, all jobs |
| faminc    | ord  | [0, 14]  | family income category                |
| mind16    | cat  | [0, 15]  | major industry                        |
| mocc10    | cat  | [0, 9]   | major occupation                      |
                    
### Selection

- drop any row with any missing value
- faminc >= 0 
- age >= 16 
- basicwgt > 0
            
One random individual is selected for each household (identified by `(hhid, hrhhid)`)
 
### Encoding

All columns are mapped to [0, max] with *consecutive values* when categorical or ordinal. Consecutiveness and starting at 0 are MST requirements.

## Reproducibility

### Task

The (private) seed used to generate a task (`train`, `background`, `targets`) is computed as:

- input:    
  1. `salt`: 8 bytes
  2. `wildcards` (team, synthesizer, epsilon, background)
- j: bytes = encode (ordered) `wildcards` (using encode of json.dumps with sort_keys)
- h: 32 bytes = black2s(j, digest_size=4, salt=`salt`).digest()
- bytes h to int (big order)

## Tasks

### Content

- train: random sample (without replace) of 10000 rows from data
- background: random sample (wo replace) of % of train
- targets: random sample of 100 rows from (data \ background) with equal prob of train membership
- truth:
- synth: 

### Synthesizers

#### Changelog

- PateGan and PrivBayes: https://github.com/snake-challenge/synthetic_data_release
  - create package (sub directory, fix imports, pyproject)
  - fix encoding when categorical values are not strings
- CopulaShirley: https://github.com/snake-challenge/copula-shirley
  - create package (sub directory, fix imports, pyproject)
  - replaced R dependency (r-vinecopulib) with python wrapper pyvinecopulib
- MST: https://github.com/snake-challenge/private-pgm
  - fixed warning

#### Parameters

## Scoring

### Task
    
MembershipAdvantage = TruePositiveRate - FalsePositiveRate

### Track

...