import pandas as pd
from copula_shirley.preprocess import PreprocessData
from copula_shirley.transform import GetECDFs
from copula_shirley.transform import SampleForVine
from copula_shirley.transform import TransformToPseudoObservations
from copula_shirley.vine import GetSamplesFromVine
from copula_shirley.vine import GetSamplesFromVineOHE
from copula_shirley.vine import GetVineStructure

from synthetic_data_release.generative_models.generative_model import GenerativeModel


class CopulaShirley(GenerativeModel):
    def __init__(
        self,
        datetime_attributes,
        categorical_attributes,
        constant_cols,
        constant_vals,
        epsilon=1.0,
        categorical_encoder="ORD",
        cat_encoder_target=None,
        dp_mechanism="Laplace",
        dp_global_sens=2,
        dp_gaussian_delta=None,
        vine_sample_ratio=0.5,
        vine_family_set="all",
        vine_par_method="mle",
        vine_nonpar_method="constant",
        vine_selcrit="aic",
        vine_trunc_lvl=None,
        vine_tree_crit="tau",
        n_cores=1,
    ):
        self.datatype = pd.DataFrame
        self.multiprocess = True

        self.datetime_attributes = datetime_attributes
        self.categorical_attributes = categorical_attributes
        self.constant_cols = constant_cols
        self.constant_vals = constant_vals
        self.categorical_encoder = categorical_encoder
        self.cat_encoder_target = cat_encoder_target
        self.epsilon = epsilon
        self.dp_mechanism = dp_mechanism
        self.dp_global_sens = dp_global_sens
        self.dp_gaussian_delta = dp_gaussian_delta
        self.vine_sample_ratio = vine_sample_ratio
        self.vine_family_set = vine_family_set
        self.vine_par_method = vine_par_method
        self.vine_nonpar_method = vine_nonpar_method
        self.vine_selcrit = vine_selcrit
        self.vine_trunc_lvl = vine_trunc_lvl
        self.vine_tree_crit = vine_tree_crit
        self.n_cores = n_cores

        self.feature_names_ = None
        self.rvine_struct_ = None
        self.dp_ecdfs_ = None
        self.decoder_ = None

    def fit(self, data):
        train_index = data.sample(frac=0.8).index
        encoder_index = data.drop(train_index).index
        clean_data, self.decoder_ = PreprocessData(
            data,
            train_idx=train_index,
            test_idx=encoder_index,
            cat_encoder=self.categorical_encoder,
            cat_attr=self.categorical_attributes,
            datetime_attr=self.datetime_attributes,
            enc_target=self.cat_encoder_target,
        )

        self.feature_names_ = clean_data.columns

        vine_train_samples, ecdf_train_samples = SampleForVine(
            clean_data, self.vine_sample_ratio, 2
        )

        self.dp_ecdfs_ = GetECDFs(
            ecdf_train_samples,
            epsilon=self.epsilon,
            mechanism=self.dp_mechanism,
            GS=self.dp_global_sens,
            delta=self.dp_gaussian_delta,
        )
        pseudo_obs = TransformToPseudoObservations(vine_train_samples, self.dp_ecdfs_)

        self.rvine_struct_ = GetVineStructure(
            pseudo_obs,
            vine_family_set=self.vine_family_set,
            vine_par_method=self.vine_par_method,
            vine_nonpar_method=self.vine_nonpar_method,
            vine_selcrit=self.vine_selcrit,
            vine_trunc_lvl=self.vine_trunc_lvl,
            vine_tree_crit=self.vine_tree_crit,
            vine_cores=self.n_cores,
        )

    def generate_samples(self, nsamples):
        if self.categorical_encoder == "OHE":
            synth_samples = GetSamplesFromVineOHE(
                self.rvine_struct_,
                n_sample=nsamples,
                col_names=self.feature_names_,
                decoder=self.decoder_,
                dp_ecdfs=self.dp_ecdfs_,
                constant_cols=self.constant_cols,
                constant_vals=self.constant_vals,
                vine_cores=self.n_cores,
            )
        else:
            synth_samples = GetSamplesFromVine(
                self.rvine_struct_,
                n_sample=nsamples,
                col_names=self.feature_names_,
                dp_ecdfs=self.dp_ecdfs_,
                vine_cores=self.n_cores,
            )

        synth = self.decoder_(synth_samples)
        return synth


class MyCopulaShirley(CopulaShirley):
    CATEGORICAL_ATTRIBUTES = [
        "agechild",
        "citistat",
        "female",
        "married",
        "wbhaom",
        "cow1",
        "ftptstat",
        "statefips",
        "mind16",
        "mocc10",
        "gradeatn",
        "faminc",
    ]

    def __init__(self, **kwargs):
        super().__init__(
            datetime_attributes=[],
            categorical_attributes=self.CATEGORICAL_ATTRIBUTES,
            constant_cols=[],
            constant_vals=[],
            **kwargs
        )
