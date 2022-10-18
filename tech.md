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

## Scoring


### Task
    
MembershipAdvantage = TruePositiveRate - FalsePositiveRate

### Track

...