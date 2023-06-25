FROM mambaorg/micromamba:latest

RUN micromamba config set channel_priority strict && \
    micromamba install --yes --name base --channel conda-forge --channel bioconda snakemake && \
    micromamba clean --all --yes

USER root
RUN apt-get update && apt-get install -y gcc g++ git wget zip && \
    rm -rf /var/lib/apt/lists/*
USER $MAMBA_USER

ENTRYPOINT ["/usr/local/bin/_entrypoint.sh", "snakemake", "--cores", "--use-conda"]
