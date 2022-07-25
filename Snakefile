import json
from hashlib import blake2s
from itertools import product
from pathlib import Path

import pandas as pd
from snakemake.utils import Paramspace


configfile: "config/config.yaml"
configfile: "config/teams.yaml"
configfile: "config/space.yaml"
configfile: "config/opt.yaml"


# generate a secret (8 random bytes) to salt hashes of wildcards used as seed for task
rule secret_salt:
    output:
        protected("salt.secret"),
    shell:
        """shred -s 8 - > {output}"""


# load secret if exists
if (p := Path(rules.secret_salt.output[0])).is_file():
    logger.warning(f"Using secret from {p}.")
    secret = p.read_bytes()
else:
    logger.warning(f"Using empty secret.")
    secret = b""

# combine teams and tasks
paramspace = Paramspace(
    pd.merge(
        pd.DataFrame(config["teams"].items(), columns=["team", "algorithm"]),
        pd.DataFrame(
            product(*config["space"].values()), columns=config["space"].keys()
        ),
    )
)


def wildcards2seed(wildcards, salt=secret):
    """hash wildcards into uint < 2^32"""
    return int.from_bytes(
        blake2s(
            json.dumps(dict(wildcards), sort_keys=True).encode(),
            digest_size=4,
            salt=salt,
        ).digest(),
        "big",
    )


rule download_cpsbasic:
    output:
        "results/epi_cpsbasic_2000_2022.zip",


rule prepare_cpsbasic:
    input:
        rules.download_cpsbasic.output,
    output:
        "results/cpsbasic.feather",
    script:
        "scripts/prepare_cpsbasic.py"


rule cpsbasic_csv:
    input:
        "results/cpsbasic.feather",
    output:
        "results/data.csv",
    run:
        pd.read_feather(input[0]).to_csv(output[0], index=False)


rule prepare_task:
    input:
        rules.prepare_cpsbasic.output,
    output:
        train=f"results/{paramspace.wildcard_pattern}/train.csv",
        background=f"results/{paramspace.wildcard_pattern}/background.csv",
        targets=f"results/{paramspace.wildcard_pattern}/targets.csv",
        truth=f"results/{paramspace.wildcard_pattern}/truth.txt",
    params:
        seed=wildcards2seed,
        n_samples=config["n_samples"],
        n_targets=config["n_targets"],
        task=paramspace.instance,
    script:
        "scripts/prepare_task.py"


def synth_wrapper_params(wildcards):
    instance = paramspace.instance(wildcards)

    algorithm = instance["algorithm"]
    n_samples = config["n_samples"]
    epsilon = instance["epsilon"]
    opt = json.dumps(config["opt"][algorithm])

    return f"{algorithm} {n_samples} {epsilon} '{opt}'"


rule task_synth:
    input:
        rules.prepare_task.output.train,
    output:
        f"results/{paramspace.wildcard_pattern}/synth.csv",
    log:
        f"logs/{paramspace.wildcard_pattern}/synth.log",
    benchmark:
        f"benchmarks/{paramspace.wildcard_pattern}/synth.tsv"
    conda:
        "envs/synthesizers.yaml"
    params:
        synth_wrapper_params,
    resources:
        gpu=1,
    threads: workflow.cores  # all cores
    shell:
        """(python -m synthesizers.wrapper {input} {output} {params}) >{log} 2>&1"""


# TODO: demo!
# rule task_attack:
#     input:
#         data=f"results/data.csv",
#         synth=f"results/{paramspace.wildcard_pattern}/synth.csv",
#         background=f"results/{paramspace.wildcard_pattern}/background.csv",
#         targets=f"results/{paramspace.wildcard_pattern}/targets.csv",
#     output:
#         f"results/{paramspace.wildcard_pattern}/attack.txt",
#     params:
#         task=paramspace.instance,


rule task_attack_random:
    output:
        f"results/{paramspace.wildcard_pattern}/attack.txt",
    params:
        n_targets=config["n_targets"],
    shell:
        "shuf -r -i 0-1 -n {params.n_targets} > {output}"


rule task_scores:
    input:
        attack=f"results/{paramspace.wildcard_pattern}/attack.txt",
        truth=rules.prepare_task.output.truth,
    output:
        f"results/{paramspace.wildcard_pattern}/scores.csv",
    params:
        task=paramspace.instance,
    script:
        "scripts/score_task.py"


rule merge_scores:
    input:
        expand("results/{params}/scores.csv", params=paramspace.instance_patterns),
    output:
        "results/scores.csv",
    shell:
        """(head -n1 {input[0]}; echo {input} | xargs -n1 sed -n '2{{p;q}}') > {output}"""


rule rank_scores:
    input:
        rules.merge_scores.output,
    output:
        "results/ranking.csv",
    script:
        "scripts/rank_scores.py"


rule:
    input:
        expand(
            "results/{params}/{name}",
            params=paramspace.instance_patterns,
            name=["synth.csv", "background.csv", "targets.csv"],
        ),
        rules.rank_scores.output,
    default_target: True
