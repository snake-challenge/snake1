from synthetic_data_release.generative_models.pate_gan import PATEGAN

from synthesizers.utils import METADATA_SYNTHETIC_DATA_RELEASE


class MyPATEGAN(PATEGAN):
    def __init__(
        self,
        *,
        epsilon=1.0,
        delta=1e-5,
        infer_ranges=False,
        num_teachers=10,
        n_iters=100,
        batch_size=128,
        learning_rate=1e-4,
        multiprocess=True,
    ):
        super().__init__(
            metadata=METADATA_SYNTHETIC_DATA_RELEASE,
            eps=epsilon,
            delta=delta,
            infer_ranges=infer_ranges,
            num_teachers=num_teachers,
            n_iters=n_iters,
            batch_size=batch_size,
            learning_rate=learning_rate,
            multiprocess=multiprocess,
        )


if __name__ == "__main__":
    from synthesizers.utils import train_gen_score

    n_samples = 1000

    epsilon = 1.0
    delta = 1e-5
    num_teachers = 10
    n_iters = 100
    batch_size = 128
    learning_rate = 1e-4

    model = MyPATEGAN(
        epsilon=epsilon,
        delta=delta,
        num_teachers=num_teachers,
        n_iters=n_iters,
        batch_size=batch_size,
        learning_rate=learning_rate,
    )

    scores = train_gen_score(n_samples, model)
    for k, v in scores.items():
        print(f"{k}: {v}")
