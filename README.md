# wampyre - configuration tools for WAM wave model


## Examples

### Convert netCDF bathymetry to WAM ASCII format

__TBD__

### Convert WAM ASCII bathymetry to netCDF format

__TBD__

### Convert xyz ASCII bathymetry to WAM ASCII format

```python
from wampyre import *

b = Bathymetry.read_ascii_xyz('bathymetry_HKI.xyz', land_mask_value=0.0)
b.write_ascii_wamtopo(outfile='wamtopo_new.asc')
```

### Plot bathymetry

Create an interactive plot

```python
plot_bathymetry(b)
```

Save to a `PNG` file

```python
plot_bathymetry(b, imgfile='bathymetry_HKI.png')
```
