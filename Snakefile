import pandas as pd
from snakemake.utils import Paramspace

# TODO: move constants to config

SEED = 123

SYNTHESIZER = ["CopulaShirley", "MST", "PateGan", "PrivBayes"]
EPSILON = [0.1, 1.0, 10]
BACKGROUND = [0.0, 0.5]

# TODO: read from file
teams = pd.DataFrame(
    [(s, f"team{k}_{s}") for k, s in enumerate(SYNTHESIZER * 2)],
    columns=["synthesizer", "team"],
)

space = pd.MultiIndex.from_product(
    [SYNTHESIZER, EPSILON, BACKGROUND], names=["synthesizer", "epsilon", "background"]
).to_frame()

tasks = (
    space.set_index("synthesizer").join(teams.set_index("synthesizer")).reset_index()
)

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
        seed=SEED,
    shell:
        "snake1 prepare --n-jobs -1 --seed {params.seed} {input} {output}"


rule task:
    input:
        *rules.prepare_data.output,
    output:
        expand(
            f"tasks/{paramspace.wildcard_pattern}/{{f}}",
            f=["background.csv", "synth.csv", "targets.csv", "train.csv", "truth.csv"],
            allow_missing=True,
        ),
    shell:
        """snake1 task --synthesizer {wildcards.synthesizer} --epsilon {wildcards.epsilon} \
        --background-frac {wildcards.background} {input} $(dirname {output[0]})"""


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
