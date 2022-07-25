import itertools
from math import log1p, exp

import networkx as nx
import numpy as np
import pandas as pd
from disjoint_set import DisjointSet
from mbi import Domain, Dataset, FactoredInference
from scipy.special import logsumexp
from synthetic_data_release.generative_models.generative_model import GenerativeModel
from scipy import sparse


class MST(GenerativeModel):
    def __init__(self, domain, min_, epsilon=1.0, delta=1.0e-9):
        self.datatype = pd.DataFrame
        self.multiprocess = True

        self.domain = Domain.fromdict(domain)
        self.min_vals = min_
        self.epsilon = epsilon
        self.delta = delta

        self.est_ = None
        self.supports_ = None

    def fit(self, data):
        ds = Dataset(data, self.domain)
        rho = self.cdp_rho(self.epsilon, self.delta)
        sigma = np.sqrt(3 / (2 * rho))
        cliques = [(col,) for col in ds.domain]
        log1 = self.measure(ds, cliques, sigma)
        ds, log1, self.supports_ = self.compress_domain(ds, log1)
        cliques = self.select(ds, rho / 3.0, log1)
        log2 = self.measure(ds, cliques, sigma)
        engine = FactoredInference(ds.domain, iters=5000)
        self.est_ = engine.estimate(log1 + log2)

    def generate_samples(self, nsamples):
        synth = self.est_.synthetic_data(nsamples)
        synth = self.reverse_data(synth, self.supports_)
        synth = synth.df + self.min_vals  # rescale
        return synth

    @staticmethod
    def cdp_rho(eps, delta):
        assert eps >= 0
        assert delta > 0
        if delta >= 1:
            return 0.0  # if delta>=1 anything goes
        rhomin = 0.0  # maintain cdp_delta(rho,eps)<=delta
        rhomax = eps + 1  # maintain cdp_delta(rhomax,eps)>delta
        for i in range(1000):
            rho = (rhomin + rhomax) / 2
            if MST.cdp_delta(rho, eps) <= delta:
                rhomin = rho
            else:
                rhomax = rho
        return rhomin

    @staticmethod
    def cdp_delta(rho, eps):
        assert rho >= 0
        assert eps >= 0
        if rho == 0:
            return 0  # degenerate case

        # search for best alpha
        # Note that any alpha in (1,infty) yields a valid upper bound on delta
        # Thus if this search is slightly "incorrect" it will only result in larger delta (still valid)
        # This code has two "hacks".
        # First the binary search is run for a pre-specificed length.
        # 1000 iterations should be sufficient to converge to a good solution.
        # Second we set a minimum value of alpha to avoid numerical stability issues.
        # Note that the optimal alpha is at least (1+eps/rho)/2. Thus we only hit this constraint
        # when eps<=rho or close to it. This is not an interesting parameter regime, as you will
        # inherently get large delta in this regime.
        amin = 1.01  # don't let alpha be too small, due to numerical stability
        amax = (eps + 1) / (2 * rho) + 2
        alpha = 0  # FIX: Local variable 'alpha' might be referenced before assignment
        for i in range(1000):  # should be enough iterations
            alpha = (amin + amax) / 2
            derivative = (2 * alpha - 1) * rho - eps + log1p(-1.0 / alpha)
            if derivative < 0:
                amin = alpha
            else:
                amax = alpha
        # now calculate delta
        delta = exp((alpha - 1) * (alpha * rho - eps) + alpha * log1p(-1 / alpha)) / (
            alpha - 1.0
        )
        return min(delta, 1.0)  # delta<=1 always

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
            else:  # need to re-express measurement over the new domain
                y2 = np.append(y[sup], y[~sup].sum())
                I2 = np.ones(y2.size)
                I2[-1] = 1.0 / np.sqrt(y.size - y2.size + 1.0)
                y2[-1] /= np.sqrt(y.size - y2.size + 1.0)
                I2 = sparse.diags(I2)
                new_measurements.append((I2, y2, sigma, proj))

        return MST.transform_data(data, supports), new_measurements, supports

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
            mask = df[col].eq(mx)
            if extra.size == 0:
                pass
            else:
                df.loc[mask, col] = np.random.choice(extra, mask.sum())
            df.loc[~mask, col] = idx[df.loc[~mask, col]]
        newdom = Domain.fromdict(newdom)
        return Dataset(df, newdom)

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
    def exponential_mechanism(
        q: np.ndarray, eps: float, sensitivity: float, prng=np.random, monotonic=False
    ):
        coef = 1.0 if monotonic else 0.5
        scores = coef * eps / sensitivity * q
        probas = np.exp(scores - logsumexp(scores))
        return prng.choice(q.size, p=probas)


class MyMST(MST):
    DOMAIN = {
        "age": 65,
        "agechild": 16,
        "citistat": 5,
        "female": 2,
        "married": 2,
        "ownchild": 14,
        "wbhaom": 6,
        "gradeatn": 16,
        "cow1": 8,
        "ftptstat": 9,
        "statefips": 56,
        "hoursut": 199,
        "faminc": 15,
        "mind16": 16,
        "mocc10": 10,
    }
    MIN = {
        "age": 16,
        "agechild": 0,
        "citistat": 1,
        "female": 0,
        "married": 0,
        "ownchild": 0,
        "wbhaom": 1,
        "gradeatn": 1,
        "cow1": 1,
        "ftptstat": 2,
        "statefips": 1,
        "hoursut": 0,
        "faminc": 1,
        "mind16": 1,
        "mocc10": 1,
    }

    def __init__(self, **kwargs):
        super().__init__(domain=self.DOMAIN, min_=self.MIN, **kwargs)
