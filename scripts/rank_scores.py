import pandas as pd

sm = snakemake  # noqa

scores = pd.read_csv(sm.input[0])
rankings = (
    scores
    # keep top 1 by ma for each (al, ep, bg)
    .sort_values(by="membership_advantage", ascending=False)
    .drop_duplicates(subset=["algorithm", "epsilon", "background"])
    # count num best
    .groupby("algorithm")
    .team.value_counts()
    # rank
    .groupby("algorithm")
    .rank(method="min", ascending=False)
    .astype(int)
    .rename("rank")
)
rankings.to_csv(sm.output[0])
