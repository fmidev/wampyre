from wampyre import *

# read bathymetry from xyz file to Bathymetry object
# value 0.0 is treated as a land mask value
b = Bathymetry.read_ascii_xyz('bathymetry_HKI.xyz', land_mask_value=0.0)

# print summary of bathymetry data
print(b)

# plot bathymetry, save as PNG image
plot_bathymetry(b, imgfile='bathymetry_HKI.png')

# write out in WAM ASCII format
b.write_ascii_wamtopo(outfile='wamtopo_new.asc')

# write out in netCDF format
b.write_netcdf(outfile='bathymetry.nc')

# read bathymetry from WAM ASCII file
b = Bathymetry.read_ascii_wamtopo('wamtopo_HKI.asc')

# plot bathymetry, save as PNG image
plot_bathymetry(b, imgfile='bathymetry_HKI_02.png')

# read netCDF file
b = Bathymetry.read_netcdf('bathy_meter_GOF_2017-04-25.nc')
plot_bathymetry(b, imgfile='bathymetry_GOF.png')

