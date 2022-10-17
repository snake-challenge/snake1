from copula_shirley.copulashirley import CopulaShirley as BaseCopulaShirley

from snake1.synthesizers.base import Synthesizer
from snake1.synthesizers.constants import CAT_COLUMNS, ORD_COLUMNS


class CopulaShirley(BaseCopulaShirley, Synthesizer):
    def __init__(self, epsilon: float, *args, **kwargs):
        # TODO: constants
        super().__init__(
            dp_epsilon=epsilon,
            categorical_attributes=CAT_COLUMNS + ORD_COLUMNS,
            *args,
            **kwargs
        )
