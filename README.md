# wampyre

Configuration tools for WAM wave model

## Installation

Clone sources

```
git clone https://github.com/fmidev/wampyre.git
```

Install with `pip` in virtualenv

```bash
pip install -r <path_to_wampyre_root>/requirements.txt
pip install -e <path_to_wampyre_root>/
```

Install for single user: use `pip install --user`. This will install the
package under `$HOME/.local/lib/python*.*/site-packages/`.

## Examples

### Convert netCDF bathymetry to WAM ASCII format

```python
from wampyre import *

b = Bathymetry.read_netcdf('bathymetry.nc')
b.write_ascii_wamtopo(outfile='wamtopo.asc')
```

### Convert WAM ASCII bathymetry to netCDF format

```python
from wampyre import *

b = Bathymetry.read_ascii_wamtopo('wamtopo_HKI.asc')
b.write_netcdf('bathymetry_HKI.nc')
```

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
