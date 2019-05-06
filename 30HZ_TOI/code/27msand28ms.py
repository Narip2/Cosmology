# with 27m 27s 28m 28s dataset
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
    hdu = fits.open("/media/narip/新加卷/TOI_Data/{:0>4d}/LFI_TOI_030-PTG_R2.10_OD{:0>4d}.fits".format(i,i))
    hdu2 = fits.open("/media/narip/新加卷/TOI_Data/{:0>4d}/LFI_TOI_030-SCI_R2.00_OD{:0>4d}.fits".format(i,i))

    # if OBT is zeros
    OBT_zero = np.where(hdu2[1].data.field(1) == 0)
    OBT_nonzero = np.where(hdu2[1].data.field(1) != 0)

    m27_nonzero = np.where(hdu2[2].data.field(1) != 0)
    m27_zero = np.where(hdu2[2].data.field(1) == 0)
    s27_nonzero = np.where(hdu2[3].data.field(1) != 0)
    s27_zero = np.where(hdu2[3].data.field(1) == 0)
    m28_nonzero = np.where(hdu2[4].data.field(1) != 0)
    m28_zero = np.where(hdu2[4].data.field(1) == 0)
    s28_nonzero = np.where(hdu2[5].data.field(1) != 0)
    s28_zero = np.where(hdu2[5].data.field(1) == 0)

    # effective when OBT and LF are both effective
    # wrong when any of OBT and LF wrong
    m27nonzero_index = np.union1d(OBT_nonzero,m27_nonzero)
    m27zero_index = np.intersect1d(OBT_zero,m27_zero)
    s27nonzero_index = np.union1d(OBT_nonzero,s27_nonzero)
    s27zero_index = np.intersect1d(OBT_zero,s27_zero)
    m28nonzero_index = np.union1d(OBT_nonzero,m28_nonzero)
    m28zero_index = np.intersect1d(OBT_zero,m28_zero)
    s28nonzero_index = np.union1d(OBT_nonzero,s28_nonzero)
    s28zero_index = np.intersect1d(OBT_zero,s28_zero)

    thetas27m = hdu[2].data.field(0)
    phis27m = hdu[2].data.field(1)
    index27m = hp.ang2pix(nside,thetas27m,phis27m)
    thetas27s = hdu[3].data.field(0)
    phis27s = hdu2[3].data.field(1)
    index27s = hp.ang2pix(nside,thetas27s,phis27s)
    thetas28m = hdu[4].data.field(0)
    phis28m = hdu[4].data.field(1)
    index28m = hp.ang2pix(nside,thetas28m,phis28m)
    thetas28s = hdu[5].data.field(0)
    phis28s = hdu[5].data.field(1)
    index28s = hp.ang2pix(nside,thetas28s,phis28s)



    values1 = hdu2[2].data.field(0)
    values2 = hdu2[3].data.field(0)
    values3 = hdu2[4].data.field(0)
    values4 = hdu2[5].data.field(0)

    values1[m27nonzero_index] = 0
    values2[s27nonzero_index] = 0
    values3[m28nonzero_index] = 0
    values4[s28nonzero_index] = 0

    np.add.at(hpxmap,index27m,values1)
    np.add.at(hpxmap,index27s,values2)
    np.add.at(hpxmap,index28m,values3)
    np.add.at(hpxmap,index28s,values4)

    np.add.at(pixcount,index27m[m27zero_index],1)
    np.add.at(pixcount,index27s[s27zero_index],1)
    np.add.at(pixcount,index28m[m28zero_index],1)
    np.add.at(pixcount,index28s[s28zero_index],1)


nonzero = np.nonzero(pixcount)
np.divide.at(hpxmap,nonzero,pixcount[nonzero])
# for i in range(0,npix):
#     if(pixcount[i] != 0):
#         hpxmap[i] = hpxmap[i]/pixcount[i]

hp.mollview(hpxmap, norm='hist')
plt.show()
