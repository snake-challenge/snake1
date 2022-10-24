import json
from hashlib import blake2s
from pathlib import Path

import pandas as pd
from snakemake.utils import Paramspace

import snake1.task

# TODO: move constants to config

configfile: "config.yaml"

# TODO: read from file
teams = pd.DataFrame(
    [(s, f"team{k}_{s}") for k, s in enumerate(config["space"]["synthesizer"] * 2)],
    columns=["synthesizer", "team"],
)

space = pd.MultiIndex.from_product(config["space"].values(), names=config["space"].keys()).to_frame()

tasks = (space.set_index("synthesizer").join(teams.set_index("synthesizer")).reset_index())

paramspace = Paramspace(tasks, filename_params=space.columns.tolist())
# team~{team}/synthesizer~{synthesizer}_epsilon~{epsilon}_background~{background}

rule download_data:
    output:
        protected("epi_cpsbasic.tar.gz"),
    shell:
        "wget https://microdata.epi.org/epi_cpsbasic.tar.gz -O {output}"


rule extract_data:
    input:
        *rules.download_data.output,
    output:
        protected(
            expand("epi_cpsbasic/epi_cpsbasic_{year}.feather", year=range(2003, 2022))
        ),
    shell:
        """tar -vxf {input} -C $(dirname {output[0]}) --use-compress-program=pigz -T <(echo {output} | 
        xargs -d' ' -n1 basename)"""


rule prepare_data:
    input:
        *rules.extract_data.output,
    output:
        protected("data.feather"),
    params:
        seed=config["seed"],
    shell:
        "snake1 prepare --n-jobs -1 --seed {params.seed} {input} {output}"

rule secret:
    output:
        protected("secret.dat")
    shell:
        "shred -s 8 - > {output}"

def wildcards2seed(wildcards, key=b"", salt=b""):
    return int.from_bytes(
        blake2s(
            json.dumps(dict(wildcards), sort_keys=True).encode(),
            digest_size=4,
            key=key,
            salt=salt,
        ).digest(),
        "big",
    )


rule task:
    input:
        rules.prepare_data.output[0],
        rules.secret.output
    output:
        expand(
            f"tasks/{paramspace.wildcard_pattern}/{{f}}",
            f=["background.csv", "synth.csv", "targets.csv", "train.csv", "truth.csv"],
            allow_missing=True,
        ),
    params:
        seed=lambda wildcards, input: wildcards2seed(wildcards, Path(input[1]).read_bytes()),
    shell:
        """
        snake1 task \
        --seed {params.seed} \
        --synthesizer {wildcards.synthesizer} \
        --epsilon {wildcards.epsilon} \
        --background-frac {wildcards.background} \
        {input[0]} \
        $(dirname {output[0]})
        """


# TODO: delete testing rule
rule demo_attack:
    output:
        expand("tasks/{t}/attack.txt", t=paramspace.instance_patterns),
    shell:
        """
        for f in {output}
        do
            shuf -r -i 0-1 -n 100 > $f
        done
        """


rule tasks:
    output:
        expand("tasks/{t}/synth.csv", t=paramspace.instance_patterns),


rule score:
    input:
        expand(
            f"tasks/{paramspace.wildcard_pattern}/{{f}}",
            f=["truth.csv", "attack.txt"],
            allow_missing=True,
        ),
    output:
        f"tasks/{paramspace.wildcard_pattern}/score.txt",
    params:
        t=lambda wildcards: ",".join(map(str, paramspace.instance(wildcards).values())),
    shell:
        "(echo -n '{params.t},'; snake1 score {input}) > {output}"


rule scores:
    input:
        expand(
            f"tasks/{paramspace.wildcard_pattern}/score.txt",
            zip,
            **glob_wildcards(
                f"tasks/{paramspace.wildcard_pattern}/attack.txt"
            )._asdict(),
        ),
    output:
        "scores.csv",
    shell:
        """
        (echo "team,synthesizer,epsilon,background,score"; cat {input}) > {output}
        """


# TODO: template and render scores.csv
# TODO: secret create and use
