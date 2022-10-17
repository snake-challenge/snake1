from synthetic_data_release.generative_models.data_synthesiser import PrivBayes as Base

from snake1.synthesizers.base import Synthesizer
from snake1.synthesizers.constants import METADATA


class PrivBayes(Base, Synthesizer):
    def __init__(self, *args, **kwargs):
        super().__init__(metadata=METADATA, *args, **kwargs)

    def sample(self, n_samples):
        return self.generate_samples(n_samples)
