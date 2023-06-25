import os
from zipfile import ZipFile


configfile: "config.yaml"


wildcard_constraints:
    **{k: r"|".join(map(str, v)) for k, v in config["tasks"].items()},
    phase=r"|".join(config["phases"]),


rule download_data:
    output:
        "epi_cpsbasic_2000_2023.zip",
    params:
        url="https://microdata.epi.org/epi_cpsbasic_2000_2023.zip",
    shell:
        "wget {params.url} -O {output}"


rule prepare_data:
    input:
        rules.download_data.output[0],
    output:
        data="base.parquet",
        meta="meta.json",
    conda:
        "envs/pandas.yaml"
    params:
        chunksize=100000,
    script:
        "scripts/prepare_data.py"


rule task_prep:
    input:
        rules.prepare_data.output.data,
    output:
        train="private_data/{phase}/{generator}_{epsilon}_train.feather",
        seed="private_data/{phase}/{generator}_{epsilon}_seed.json",
        targets="public_data/{phase}/{generator}_{epsilon}_targets.csv",
        targets_idx="public_data/{phase}/{generator}_{epsilon}_targets_index.txt",
        truth="reference_data/{phase}/{generator}_{epsilon}/{generator}_{epsilon}.txt",
    conda:
        "envs/pandas.yaml"
    params:
        target_min_hh=config["target_min_hh"],
        n_samples=config["n_samples"],
        n_targets=config["n_targets"],
    script:
        "scripts/task_prep.py"


rule task_synth:
    input:
        train=rules.task_prep.output.train,
        meta=rules.prepare_data.output.meta,
    output:
        synth="public_data/{phase}/{generator}_{epsilon}_synthetic.csv",
    shadow:
        "shallow"
    conda:
        "envs/reprosyn.yaml"
    params:
        generator=lambda wildcards: wildcards.generator.upper(),
        epsilon=lambda wildcards: float(wildcards.epsilon),
        n_samples=config["n_samples"],
    script:
        "scripts/task_synth.py"


rule task_hash:
    input:
        rules.task_synth.output.synth,
        rules.task_prep.output.train,
        rules.task_prep.output.seed,
        rules.task_prep.output.targets,
        rules.task_prep.output.targets_idx,
        rules.task_prep.output.truth,
    output:
        "public_data/{phase}/{generator}_{epsilon}.sha512",
    shell:
        "sha512sum {input} > {output}"


rule attack_random:
    input:
        rules.task_prep.output.targets_idx,
    output:
        "starting_kit/{phase}/{generator}_{epsilon}.txt",
    script:
        "scripts/attack_random.py"


rule competition_config:
    output:
        "competition.yaml",
    params:
        tasks=config["tasks"],
        phases=config["phases"],
        max_submissions_per_day=config["max_submissions_per_day"],
        max_submissions=config["max_submissions"],
    script:
        "scripts/competition_config.py"


rule _zip:
    input:
        [],
    output:
        [],
    shell:
        "zip {output} {input}"


rule _zip_skip_commonpath:
    input:
        [],
    output:
        [],
    run:
        prefix = os.path.commonpath(input)
        with ZipFile(output[0], "w") as zf:
            for i in input:
                zf.write(i, os.path.relpath(i, prefix))


use rule _zip_skip_commonpath as public_zip with:
    input:
        expand(
            [
                rules.task_synth.output.synth,
                rules.task_prep.output.targets,
                rules.task_prep.output.targets_idx,
                rules.task_hash.output[0],
            ],
            **config["tasks"],
            allow_missing=True
        ),
    output:
        "public_data_{phase}.zip",


use rule _zip as private_zip with:
    input:
        expand(
            [
                rules.task_prep.output.truth,
                rules.task_prep.output.train,
                rules.task_prep.output.seed,
            ],
            **config["tasks"],
            allow_missing=True
        ),
    output:
        "private_data_{phase}.zip",


use rule _zip_skip_commonpath as starting_kit_zip with:
    input:
        expand(rules.attack_random.output[0], **config["tasks"], allow_missing=True),
    output:
        "starting_kit_{phase}.zip",



use rule _zip as bundle_zip with:
    input:
        "competition.yaml",
        "logo.png",
        "pages/data.md",
        "pages/evaluation.md",
        "pages/getting_started.md",
        "pages/overview.md",
        "pages/terms.md",
        "scoring_program/metadata.yaml",
        "scoring_program/score.py",
        expand(rules.task_prep.output.truth, phase=config["phases"], **config["tasks"]),
    output:
        "bundle.zip",


rule all:
    default_target: True
    input:
        rules.bundle_zip.output[0],
        expand(
            [
                rules.private_zip.output[0],
                rules.public_zip.output[0],
                rules.starting_kit_zip.output[0],
            ],
            phase=config["phases"],
        ),
