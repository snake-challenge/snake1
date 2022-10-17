from synthetic_data_release.generative_models.pate_gan import PATEGAN as Base

from snake1.synthesizers.base import Synthesizer
from snake1.synthesizers.constants import METADATA


class PateGan(Base, Synthesizer):
    def __init__(self, epsilon: float, *args, **kwargs):
        super().__init__(metadata=METADATA, eps=epsilon, *args, **kwargs)

    def sample(self, n_samples):
        return self.generate_samples(n_samples)
