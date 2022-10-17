import itertools
from functools import partial

import networkx as nx
import numpy as np
from disjoint_set import DisjointSet
from mbi import Domain, Dataset, FactoredInference
from scipy import sparse
from scipy.special import logsumexp

from snake1.synthesizers.base import Synthesizer
from snake1.synthesizers.constants import DOMAIN


class MST(Synthesizer):
    def __init__(self, epsilon: float, delta: float = 1e-9):
        self.domain = Domain.fromdict(DOMAIN)

        self.epsilon = epsilon
        self.delta = delta

        self.est_ = ...
        self.undo_compress_fn_ = ...

    def fit(self, data):
        data = Dataset(data, self.domain)

        rho = MST.cdp_rho(self.epsilon, self.delta)
        sigma = np.sqrt(3 / (2 * rho))
        cliques = [(col,) for col in data.domain]
        log1 = MST.measure(data, cliques, sigma)
        data, log1, self.undo_compress_fn_ = MST.compress_domain(data, log1)
        cliques = MST.select(data, rho / 3.0, log1)
        log2 = MST.measure(data, cliques, sigma)
        engine = FactoredInference(data.domain, iters=5000)
        self.est_ = engine.estimate(log1 + log2)

    def sample(self, n_samples):
        synth = self.est_.synthetic_data(n_samples)
        synth = self.undo_compress_fn_(synth).df
        return synth

    @staticmethod
    def measure(data, cliques, sigma, weights=None):
        if weights is None:
            weights = np.ones(len(cliques))
        weights = np.array(weights) / np.linalg.norm(weights)
        measurements = []
        for proj, wgt in zip(cliques, weights):
            x = data.project(proj).datavector()
            y = x + np.random.normal(loc=0, scale=sigma / wgt, size=x.size)
            Q = sparse.eye(x.size)
            measurements.append((Q, y, sigma / wgt, proj))
        return measurements

    @staticmethod
    def compress_domain(data, measurements):
        supports = {}
        new_measurements = []
        for Q, y, sigma, proj in measurements:
            col = proj[0]
            sup = y >= 3 * sigma
            supports[col] = sup
            if supports[col].sum() == y.size:
                new_measurements.append((Q, y, sigma, proj))
            else:
                y2 = np.append(y[sup], y[~sup].sum())
                I2 = np.ones(y2.size)
                I2[-1] = 1.0 / np.sqrt(y.size - y2.size + 1.0)
                y2[-1] /= np.sqrt(y.size - y2.size + 1.0)
                I2 = sparse.diags(I2)
                new_measurements.append((I2, y2, sigma, proj))
        undo_compress_fn = partial(MST.reverse_data, supports=supports)
        return MST.transform_data(data, supports), new_measurements, undo_compress_fn

    @staticmethod
    def exponential_mechanism(q, eps, sensitivity, prng=np.random, monotonic=False):
        coef = 1.0 if monotonic else 0.5
        scores = np.asarray(coef * eps / sensitivity * q)
        probas = np.exp(scores - logsumexp(scores))
        return prng.choice(q.size, p=probas)

    @staticmethod
    def select(data, rho, measurement_log, cliques=None):
        if cliques is None:
            cliques = []

        engine = FactoredInference(data.domain, iters=1000)
        est = engine.estimate(measurement_log)

        weights = {}
        candidates = list(itertools.combinations(data.domain.attrs, 2))
        for a, b in candidates:
            xhat = est.project([a, b]).datavector()
            x = data.project([a, b]).datavector()
            weights[a, b] = np.linalg.norm(x - xhat, 1)

        T = nx.Graph()
        T.add_nodes_from(data.domain.attrs)
        ds = DisjointSet()

        for e in cliques:
            T.add_edge(*e)
            ds.union(*e)

        r = len(list(nx.connected_components(T)))
        epsilon = np.sqrt(8 * rho / (r - 1))
        for i in range(r - 1):
            candidates = [e for e in candidates if not ds.connected(*e)]
            wgts = np.array([weights[e] for e in candidates])
            idx = MST.exponential_mechanism(wgts, epsilon, sensitivity=1.0)
            e = candidates[idx]
            T.add_edge(*e)
            ds.union(*e)

        return list(T.edges)

    @staticmethod
    def transform_data(data, supports):
        df = data.df.copy()
        newdom = {}
        for col in data.domain:
            support = supports[col]
            size = support.sum()
            newdom[col] = int(size)
            if size < support.size:
                newdom[col] += 1
            mapping = {}
            idx = 0
            for i in range(support.size):
                mapping[i] = size
                if support[i]:
                    mapping[i] = idx
                    idx += 1
            assert idx == size
            df[col] = df[col].map(mapping)
        newdom = Domain.fromdict(newdom)
        return Dataset(df, newdom)

    @staticmethod
    def reverse_data(data, supports):
        df = data.df.copy()
        newdom = {}
        for col in data.domain:
            support = supports[col]
            mx = support.sum()
            newdom[col] = int(support.size)
            idx, extra = np.where(support)[0], np.where(~support)[0]
            mask = df[col] == mx
            if extra.size == 0:
                pass
            else:
                df.loc[mask, col] = np.random.choice(extra, np.sum(mask))
            df.loc[~mask, col] = idx[df.loc[~mask, col]]
        newdom = Domain.fromdict(newdom)
        return Dataset(df, newdom)

    @staticmethod
    def cdp_delta_standard(rho, eps):
        assert rho >= 0
        assert eps >= 0
        if rho == 0:
            return 0

        return np.exp(-((eps - rho) ** 2) / (4 * rho))

    @staticmethod
    def cdp_delta(rho, eps):
        assert rho >= 0
        assert eps >= 0
        if rho == 0:
            return 0

        amin = 1.01
        amax = (eps + 1) / (2 * rho) + 2
        alpha = None
        for i in range(1000):
            alpha = (amin + amax) / 2
            derivative = (2 * alpha - 1) * rho - eps + np.log1p(-1.0 / alpha)
            if derivative < 0:
                amin = alpha
            else:
                amax = alpha

        delta = np.exp(
            (alpha - 1) * (alpha * rho - eps) + alpha * np.log1p(-1 / alpha)
        ) / (alpha - 1.0)
        return min(delta, 1.0)

    @staticmethod
    def cdp_eps(rho, delta):
        assert rho >= 0
        assert delta > 0
        if delta >= 1 or rho == 0:
            return 0.0
        epsmin = 0.0
        epsmax = rho + 2 * np.sqrt(rho * np.log(1 / delta))

        for i in range(1000):
            eps = (epsmin + epsmax) / 2
            if MST.cdp_delta(rho, eps) <= delta:
                epsmax = eps
            else:
                epsmin = eps
        return epsmax

    @staticmethod
    def cdp_rho(eps, delta):
        assert eps >= 0
        assert delta > 0
        if delta >= 1:
            return 0.0
        rhomin = 0.0
        rhomax = eps + 1
        for i in range(1000):
            rho = (rhomin + rhomax) / 2
            if MST.cdp_delta(rho, eps) <= delta:
                rhomin = rho
            else:
                rhomax = rho
        return rhomin
