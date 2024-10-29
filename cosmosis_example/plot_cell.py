import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits

# Got total shear Cell for auto-correlation for bin 2 as an example.
ell  = np.loadtxt('output_cosmosis_example/shear_cl/ell.txt')
cell_full = np.loadtxt('output_cosmosis_example/shear_cl/bin_2_2.txt')
cell_ii   = np.loadtxt('output_cosmosis_example/shear_cl_ii/bin_2_2.txt')
cell_gg   = np.loadtxt('output_cosmosis_example/shear_cl_gg/bin_2_2.txt')
cell_gi   = np.loadtxt('output_cosmosis_example/shear_cl_gi/bin_2_2.txt')

plt.clf()
plt.plot(ell, ell*(cell_gg+cell_ii+2.*cell_gi)*1e7, label=r'$C_{\ell}^{GG}$+$C_{\ell}^{II}$+2$C_{\ell}^{GI}$',color='red',lw=4)
plt.plot(ell, ell*cell_full*1e7, label=r'Total Shear $C_{\ell}$',color='black',lw=2)
plt.plot(ell, ell*cell_gg*1e7, label=r'Galaxy Shear $C_{\ell}^{GG}$',ls='--',color='darkgoldenrod')
plt.plot(ell, ell*cell_ii*1e7, label=r'Intrinsic $C_{\ell}^{II}$',ls='-.',color='plum')
plt.plot(ell, ell*cell_gi*1e7, label=r'Galaxy Shear x Intrinsic $C_{\ell}^{GI}$',ls='-.',color='darkorchid')
plt.legend(frameon=False)
plt.xscale('log')
plt.xlim(20,2000)
plt.ylabel(r'$10^{7}\ell C_{\ell}^{\kappa \kappa, 22}$',fontsize=15)
plt.xlabel(r'$\ell$',fontsize=15)
plt.savefig('plots/model_shear_cl.png')



lsst = fits.open('lssty10_srd_32pt_simulation.fits')
select_bin1 = lsst['shear_cl'].data['bin1'] == 2
select_bin2 = lsst['shear_cl'].data['bin2'] == 2
ell_data = lsst['shear_cl'].data['ANG'][select_bin1 & select_bin2]
cl_data = lsst['shear_cl'].data['VALUE'][select_bin1 & select_bin2]
cl_error_data = np.diag(lsst['COVMAT'].data)[15*5:15*6]

plt.clf()
plt.errorbar(ell_data, cl_data*ell_data*1e7,yerr=ell_data*np.sqrt(cl_error_data)*1e7,fmt='o',ls='none',\
    markersize=3.,color='teal',label='Simulated LSST Y10 shear data')
plt.plot(ell, ell*cell_full*1e7, label=r'Modeled LSST Y10 $C_{\ell}$',color='black',lw=2)
plt.legend(frameon=False)
plt.xscale('log')
plt.xlim(20,2000)
plt.ylabel(r'$10^{7}\ell C_{\ell}^{\kappa \kappa, 22}$',fontsize=15)
plt.xlabel(r'$\ell$',fontsize=15)
plt.savefig('plots/model_data_shear_cl.png')