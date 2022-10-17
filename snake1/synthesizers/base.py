from abc import ABC, abstractmethod
from importlib import import_module

import pandas as pd


class Synthesizer(ABC):
    @staticmethod
    def by_name(name):
        try:
            mod = import_module(".." + name.lower(), __name__)
            class_ = getattr(mod, name)
            return class_
        except (ModuleNotFoundError, AttributeError) as e:
            raise ValueError(f"No synthesizer named {name}.")

    @abstractmethod
    def fit(self, data: pd.DataFrame):
        raise NotImplementedError

    @abstractmethod
    def sample(self, n_samples: int) -> pd.DataFrame:
        raise NotImplementedError

    def fit_sample(self, data: pd.DataFrame, n_samples: int = None) -> pd.DataFrame:
        n_samples = n_samples if n_samples is not None else len(data)
        self.fit(data)
        return self.sample(n_samples)
