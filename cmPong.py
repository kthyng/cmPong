'''
PONG colormaps.

To run and then test:

> levels = (37-exp(linspace(0,log(36.), 10)))[::-1]-1
> my_cmap = cm_pong.salinity('YlGnBu', levels)
> ilevels = [0,1,2,3,4,5,8] # which levels to label
> ticks = [int(tick) for tick in levels[ilevels]]
> cm_pong.test_txla(my_cmap, ticks)
'''

import numpy as np
import matplotlib
from pylab import *
import netCDF4 as netCDF
from pyproj import Proj
import matplotlib.ticker as ticker
from mpl_toolkits.basemap import Basemap

mpl.rcParams.update({'font.size': 26})
mpl.rcParams['font.sans-serif'] = 'Arev Sans, Bitstream Vera Sans, Lucida Grande, Verdana, Geneva, Lucid, Helvetica, Avant Garde, sans-serif'
mpl.rcParams['mathtext.fontset'] = 'custom'
mpl.rcParams['mathtext.cal'] = 'cursive'
mpl.rcParams['mathtext.rm'] = 'sans'
mpl.rcParams['mathtext.tt'] = 'monospace'
mpl.rcParams['mathtext.it'] = 'sans:italic'
mpl.rcParams['mathtext.bf'] = 'sans:bold'
mpl.rcParams['mathtext.sf'] = 'sans'
mpl.rcParams['mathtext.fallback_to_cm'] = 'True'

def salinity(cmap='YlGnBu_r', levels=(37-exp(linspace(0,log(36.), 10)))[::-1]-1):
    '''
    Colormap for salinity, with bigger chunks of salinity per color
    section at lower salinity than higher.
    From http://wiki.scipy.org/Cookbook/Matplotlib/Show_colormaps

    Inputs:
        cmap        Colormap name to use, e.g. 'YlGnBu'
        levels      edges of colors, as in contourf, to stretch 
                    colormap. e.g. for salinity
                    levels = (37-exp(linspace(0,log(36.), 10)))[::-1]-1

    Outputs:
        my_cmap     colormap instance
    '''

    N = levels.size

    # Colors on either side of the edges
    rgb0 = cm.get_cmap(cmap)(linspace(0.0, 1.0, N))[:,0:3]

    red = np.vstack((levels/levels.max(), 
                    rgb0[:,0], 
                    rgb0[:,0])).T
    red = tuple(map(tuple, red))

    green = np.vstack((levels/levels.max(), 
                    rgb0[:,1], 
                    rgb0[:,1])).T
    green = tuple(map(tuple, green))

    blue = np.vstack((levels/levels.max(), 
                    rgb0[:,2], 
                    rgb0[:,2])).T
    blue = tuple(map(tuple, blue))

    cdict = {'red':red, 'green':green, 'blue':blue}

    my_cmap = matplotlib.colors.LinearSegmentedColormap('my_colormap',cdict,256)

    return my_cmap

def test_simple(cmap):
    '''
    Test colormap.
    '''

    figure()
    pcolor(rand(10,10), cmap=cmap)
    cb = colorbar()

def test_txla(my_cmap, ticks):
    '''
    Test colormap with TXLA model output
    Inputs:
        cmap    Your colormap instance
        labels  Tick locations and labels for colorbar.
    '''

    # Model output to use
    loc = 'http://barataria.tamu.edu:8080/thredds/dodsC/NcML/txla_nesting6.nc'
    d = netCDF.Dataset(loc)
    # surface salinity at random date
    salt = np.squeeze(d.variables['salt'][11304,-1,:,:])
    lonr = d.variables['lon_rho'][:]
    latr = d.variables['lat_rho'][:]
    h = d.variables['h'][:]
    d.close()

    # Basemap parameters.
    llcrnrlon=-98; llcrnrlat=27; 
    urcrnrlon=-87.5; urcrnrlat=30.5; projection='lcc'
    lat_0=29; lon_0=-94; resolution='i'; area_thresh=0.

    basemap = Basemap(llcrnrlon=llcrnrlon,
                 llcrnrlat=llcrnrlat,
                 urcrnrlon=urcrnrlon,
                 urcrnrlat=urcrnrlat,
                 projection=projection,
                 lat_0=lat_0,
                 lon_0=lon_0,
                 resolution=resolution,
                 area_thresh=area_thresh)
    xr, yr = basemap(lonr, latr)

    fig = plt.figure(figsize=(17,9))
    ax = fig.add_subplot(111)
    basemap.drawcoastlines(ax=ax)
    basemap.fillcontinents('0.8',ax=ax)
    basemap.drawparallels(np.arange(18, 35), dashes=(1, 1), 
                            linewidth=0.15, labels=[1, 0, 0, 0], ax=ax)
    basemap.drawmeridians(np.arange(-100, -80), dashes=(1, 1), 
                            linewidth=0.15, labels=[0, 0, 0, 1], ax=ax)

    ax.contour(xr, yr, h, 
                    np.hstack(([10,20],np.arange(50,500,50))), 
                    colors='lightgrey', linewidths=0.5)

    # Outline numerical domain
    ax.plot(xr[0,:], yr[0,:], 'k:')
    ax.plot(xr[-1,:], yr[-1,:], 'k:')
    ax.plot(xr[:,0], yr[:,0], 'k:')
    ax.plot(xr[:,-1], yr[:,-1], 'k:')

    # Plot surface salinity
    ax.contour(xr, yr, salt, [33], colors='k')
    mappable = ax.pcolormesh(xr, yr, salt, cmap=my_cmap, vmin=0, vmax=36)

    # Colorbar in upper left corner
    cax = fig.add_axes([0.15, 0.75, 0.3, 0.03]) #colorbar axes
    cb = colorbar(mappable, cax=cax, orientation='horizontal')
    cb.set_label('Surface salinity [g$\cdot$kg$^{-1}$]', fontsize=20)
    cb.ax.tick_params(labelsize=18) 

    # Label colorbar at stretched intervals
    cb.set_ticks(ticks)
    cb.set_ticklabels(ticks)

    fig.savefig('figures/test.png', bbox_inches='tight')