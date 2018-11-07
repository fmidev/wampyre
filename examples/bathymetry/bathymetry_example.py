from wampyre import *

# read bathymetry from xyz file to Bathymetry object
# value 0.0 is treated as a land mask value
b = read_ascii_xyz('bathymetry_HKI.xyz', land_mask_value=0.0)

# print summary of bathymetry data
print(b)

# plot bathymetry, save as PNG image
plot_bathymetry(b, imgfile='bathymetry_HKI.png')

# write out in WAM ASCII format
write_ascii_wamtopo(b, outfile='wamtopo_new.asc')

# read bathymetry from WAM ASCII file
b = read_ascii_wamtopo('wamtopo_HKI.asc')

# plot bathymetry, save as PNG image
plot_bathymetry(b, imgfile='bathymetry_HKI_02.png')

