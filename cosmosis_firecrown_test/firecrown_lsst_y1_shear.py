import os
import sacc

import firecrown.likelihood.gauss_family.statistic.source.weak_lensing as wl
from firecrown.likelihood.gauss_family.statistic.two_point import TwoPoint
from firecrown.likelihood.gauss_family.gaussian import ConstGaussian


# The likelihood used for DES Y1 3x2pt analysis is a Gaussian likelihood, which
# necessitates providing a list of statistics that are each represented by a two-point
# function. To construct the two-point function, a list of sources is required, with
# each source being responsible for computing the theoretical prediction for a specific
#  segment of the data. These sources are created using the build_likelihood function
# and also contain a list of systematics. The systematics are classes that modify the
# theoretical prediction and are also constructed in the build_likelihood function.
def build_likelihood(_):
    """Build the DES Y1 3x2pt likelihood."""
    # Creates a LAI systematic. This is a systematic that is applied to
    # all weak-lensing probes. The `sacc_tracer` argument is used to identify the
    # section of the SACC file that this systematic will be applied to. In this
    # case we want to apply it to all weak-lensing probes, so we use the
    # empty string.
    lai_systematic = wl.LinearAlignmentSystematic(sacc_tracer="")


    sources = {}
    # why wouldn't this work?

    for i in range(5):
        # Each weak-lensing section has its own multiplicative bias. Parameters
        # reflect this by using src{i}_ prefix.
        mbias = wl.MultiplicativeShearBias(sacc_tracer=f"src{i}")

        # We also include a photo-z shift bias (a constant shift in dndz). We
        # also have a different parameter for each bin, so here again we use the
        # src{i}_ prefix.
        wl_pzshift = wl.PhotoZShift(sacc_tracer=f"src{i}")

        # Now we can finally create the weak-lensing source that will compute the
        # theoretical prediction for that section of the data, given the
        # systematics.
        sources[f"src{i}"] = wl.WeakLensing(
            sacc_tracer=f"src{i}", systematics=[lai_systematic, mbias, wl_pzshift]
        )

    # Now that we have all sources we can instantiate all the two-point
    # functions. The weak-lensing sources have two "data types", for each one we
    # create a new two-point function.
    stats = {}

    # Creating all auto/cross-correlations two-point function objects for the
    # weak-lensing probes.
    for i in range(5):
        for j in range(i, 5):
            stats[f"galaxy_shear_cl_ee_src{i}_src{j}"] = TwoPoint(
                source0=sources[f"src{i}"],
                source1=sources[f"src{j}"],
                sacc_data_type="galaxy_shear_cl_ee",
            )

    # Here we instantiate the actual likelihood. The statistics argument carry
    # the order of the data/theory vector.
    likelihood = ConstGaussian(statistics=list(stats.values()))

    sacc_data = sacc.Sacc.load_fits('test_cov.sacc')

    # The read likelihood method is called passing the loaded SACC file, the
    # two-point functions will receive the appropriated sections of the SACC
    # file and the sources their respective dndz.
    likelihood.read(sacc_data)

    # This script will be loaded by the appropriated connector. The framework
    # will call the factory function that should return a Likelihood instance.
    return likelihood
