from synthetic_data_release.generative_models.data_synthesiser import PrivBayes

from synthesizers.utils import METADATA_SYNTHETIC_DATA_RELEASE


class MyPrivBayes(PrivBayes):
    def __init__(
        self,
        histogram_bins=10,
        degree=1,
        epsilon=0.1,
        infer_ranges=False,
        multiprocess=True,
        seed=None,
    ):
        super().__init__(
            metadata=METADATA_SYNTHETIC_DATA_RELEASE,
            histogram_bins=histogram_bins,
            degree=degree,
            epsilon=epsilon,
            infer_ranges=infer_ranges,
            multiprocess=multiprocess,
            seed=seed,
        )


if __name__ == "__main__":
    from synthesizers.utils import train_gen_score

    n_samples = 1000

    histogram_bins = 10
    degree = 1
    epsilon = 0.1

    model = MyPrivBayes(
        histogram_bins=histogram_bins,
        degree=degree,
        epsilon=epsilon,
    )

    scores = train_gen_score(n_samples, model)
    for k, v in scores.items():
        print(f"{k}: {v}")
