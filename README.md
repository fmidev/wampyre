# WAMpyre - config tools for WAM wave model


## Examples

### Convert netCDF bathymetry to WAM ASCII format

__TBD__

### Convert WAM ASCII bathymetry to netCDF format

__TBD__

### Convert xyz ASCII bathymetry to WAM ASCII format

```python
from wampyre import *

b = read_ascii_xyz('bathymetry_HKI.xyz', land_mask_value=0.0)
write_ascii_wamtopo(b, outfile='wamtopo_new.asc')
```

### Plot bathymetry

Create an interactive plot

```python
b = read_ascii_xyz('bathymetry_HKI.xyz', land_mask_value=0.0)
plot_bathymetry(b)
```

Save to a `PNG` file

```python
b = read_ascii_xyz('bathymetry_HKI.xyz', land_mask_value=0.0)
plot_bathymetry(b, imgfile='bathymetry_HKI.png')
```
