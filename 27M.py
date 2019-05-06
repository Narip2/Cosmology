import numpy as np
import healpy as hp
import matplotlib.pyplot as plt
from astropy.io import fits
nside = 1024
npix = hp.nside2npix(nside)
hpxmap = np.zeros(npix, dtype=np.float)
pixcount = np.zeros(npix, dtype=np.float)

for i in range(91,600):
    value = np.zeros(npix, dtype=np.float)

    if(i == 700 or i == 800 or i==900 or i == 777 or i == 605):
        continue
    hdu = fits.open("/media/narip/新加卷1/TOI_Data/{:0>4d}/LFI_TOI_030-PTG_R2.10_OD{:0>4d}.fits".format(i,i))
    hdu2 = fits.open("/media/narip/新加卷1/TOI_Data/{:0>4d}/LFI_TOI_030-SCI_R2.00_OD{:0>4d}.fits".format(i,i))

    # if OBT is zeros
    OBT_zero = np.where(hdu2[1].data.field(1) == 0)
    OBT_nonzero = np.where(hdu2[1].data.field(1) != 0)

    LF_nonzero = np.where(hdu2[2].data.field(1) != 0)
    LF_zero = np.where(hdu2[2].data.field(1) == 0)

    # effective when OBT and LF are both effective
    # wrong when any of OBT and LF wrong
    nonzero_index = np.union1d(OBT_nonzero,LF_nonzero)
    zero_index = np.intersect1d(OBT_zero,LF_zero)

    thetas = hdu[2].data.field(0)
    phis = hdu[2].data.field(1)

    index = hp.ang2pix(nside,thetas,phis)
    values = hdu2[2].data.field(0)
    np.add.at(values,nonzero_index,-values[nonzero_index])

    np.add.at(hpxmap,index,values)
    np.add.at(pixcount,index[zero_index],1)




nonzero = np.nonzero(pixcount)
np.divide.at(hpxmap,nonzero,pixcount[nonzero])
# for i in range(0,npix):
#     if(pixcount[i] != 0):
#         hpxmap[i] = hpxmap[i]/pixcount[i]

hp.mollview(hpxmap, norm='hist')
plt.show()
