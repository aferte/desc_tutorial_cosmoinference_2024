# We define here all the details about the modeling and the likelihood
# for firecrown.
import os
import sacc

import firecrown.likelihood.gauss_family.statistic.source.weak_lensing as wl
from firecrown.likelihood.gauss_family.statistic.two_point import TwoPoint
from firecrown.likelihood.gauss_family.gaussian import ConstGaussian


def build_likelihood(_):

    # Define our systematics
    ## NLA IA
    lai_systematic = wl.LinearAlignmentSystematic(sacc_tracer="")
    ## shear bias
    mbias = wl.MultiplicativeShearBias(sacc_tracer=f"src1")
    ## photoz bias
    wl_pzshift = wl.PhotoZShift(sacc_tracer=f"src1")

    # We create here the sources that will enter the cosmic shear correlation
    # function. They are based on a tracer, which says which galaxies
    # are contributing. Here we want shear for galaxies in bin 1.
    sources = {}
    sources[f"src1"] = wl.WeakLensing(
        sacc_tracer=f"src1", systematics=[lai_systematic, mbias, wl_pzshift]
    )

    # Yay now we can compute the actual shear correlation function.
    stats = {}
    stats[f"galaxy_shear_cl_ee_src1_src1"] = TwoPoint(
        source0=sources[f"src1"],
        source1=sources[f"src1"],
        sacc_data_type="galaxy_shear_cl_ee",
    )

    # And now compute the likelihood for the above shear prediction.
    likelihood = ConstGaussian(statistics=list(stats.values()))

    sacc_data = sacc.Sacc.load_fits('temp_cov.sacc')
    likelihood.read(sacc_data)

    return likelihood
