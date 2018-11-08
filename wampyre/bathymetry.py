"""
Tools for reading/writing/plotting WAM bathymetry files
"""
import numpy
import matplotlib.pyplot as plt
import textwrap


class Bathymetry(object):
    """
    A simple bathymetry object.
    """
    def __init__(self, lon, lat, depth, land_mask=None):
        self.lat = lat
        self.lon = lon
        self.depth = numpy.ma.masked_array(depth, mask=land_mask)

        dx_lon = numpy.diff(self.lon)
        assert numpy.all(numpy.abs(dx_lon - dx_lon[0]) < 1e-6), \
            'Lon must be equally spaced'
        dx_lat = numpy.diff(self.lat)
        assert numpy.all(numpy.abs(dx_lat - dx_lat[0]) < 1e-6), \
            'Lat must be equally spaced'
        self.dx_lon = numpy.round(numpy.mean(dx_lon), 14)
        self.dx_lat = numpy.round(numpy.mean(dx_lat), 14)
        nlon = len(self.lon)
        nlat = len(self.lat)
        msg = 'Depth array has wrong shape. Expected {:}, found {:}'
        shape = (nlon, nlat)
        assert depth.shape == shape, msg.format(shape, depth.shape)
        assert numpy.all(depth >= 0.0), 'Depth must be non-negative'

    def __str__(self):
        out = ''
        out += 'Bathymetry\n'
        out += 'Lon {:} {:} ({:}) dx={:}\n'.format(self.lon[0], self.lon[-1],
                                                   len(self.lon), self.dx_lon)
        out += 'Lat {:} {:} ({:}) dx={:}\n'.format(self.lat[0], self.lat[-1],
                                                   len(self.lat), self.dx_lat)
        out += 'Depth: {:} {:}'.format(self.depth.max(), self.depth.min())
        return out

    @classmethod
    def read_ascii_xyz(cls, xyz_file, land_mask_value=None):
        """
        Reads bathymetry from an ASCII file

        File is assumed to read
        lon, lat, depth
        lon, lat, depth
        ...
        """
        print('Reading file {:}'.format(xyz_file))
        xyz = numpy.loadtxt(xyz_file, dtype=numpy.float64)

        lon = xyz[:, 0]
        lat = xyz[:, 1]
        dep = xyz[:, 2]
        # depth should be positive
        dep *= -1

        # find unique lon,lat entries
        # these are in ascending order
        lon_unique, lon_rev_ix = numpy.unique(lon, return_inverse=True)
        lat_unique, lat_rev_ix = numpy.unique(lat, return_inverse=True)

        nlon = len(lon_unique)
        nlat = len(lat_unique)

        dep_array = numpy.zeros((nlon, nlat))

        for i in range(len(dep)):
            dep_array[lon_rev_ix[i], lat_rev_ix[i]] = dep[i]

        land_mask = None
        if land_mask_value is not None:
            land_mask = dep_array == land_mask_value
        return cls(lon_unique, lat_unique, dep_array, land_mask=land_mask)

    @classmethod
    def read_ascii_wamtopo(cls, topo_file):
        """
        Reads bathymetry from WAM topography ASCII file

        File is assumed to read
        lon, lat, depth
        lon, lat, depth
        ...
        """
        print('Reading file {:}'.format(topo_file))
        mask = []
        values = []
        with open(topo_file, 'r') as f:

            def parse_entry(s):
                land_mask = True if 'E' in s else False
                value = float(s[:-1])
                return value, land_mask

            header = f.readline()
            grid_vals = [float(f) for f in header.split()]
            dx_lat, dx_lon, lat_min, lat_max, lon_min, lon_max = grid_vals
            for line in f.readlines():
                for s in line.split():
                    v, m = parse_entry(s)
                    values.append(v)
                    mask.append(m)
        mask = numpy.array(mask, dtype=bool)
        values = numpy.array(values, dtype=float)

        nlon = int(numpy.round((lon_max - lon_min)/dx_lon)) + 1
        nlat = int(numpy.round((lat_max - lat_min)/dx_lat)) + 1
        lon = numpy.linspace(lon_min, lon_max, nlon)
        lat = numpy.linspace(lat_min, lat_max, nlat)

        values = numpy.reshape(values, (nlat, nlon)).T
        mask = numpy.reshape(mask, (nlat, nlon)).T
        return cls(lon, lat, values, land_mask=mask)

    def write_ascii_wamtopo(self, outfile='wamtopo.asc'):
        """
        Writes bathymetry to disk in WAM ASCII format.
        """
        print('Writing WAM ASCII to {:}'.format(outfile))

        def stringify_value(args):
            v, mask = args
            char = 'E' if mask else 'D'
            return '{: 5d}'.format(v) + char

        with open(outfile, 'w') as f:
            header = ' {:.9f} {:.9f} {:11.7f} {:11.7f} {:11.7f} {:11.7f}\n'.format(
                self.dx_lat, self.dx_lon,
                self.lat.min(), self.lat.max(), self.lon.min(), self.lon.max())
            f.write(header)
            dep = self.depth
            mask = dep.mask
            dep = dep.filled(0.0)
            for line, mask in zip(dep.T, mask.T):
                val_str = map(stringify_value, zip(line.astype(int), mask))
                val_str = ''.join(val_str)
                output = textwrap.fill(val_str, width=12*6, drop_whitespace=False)
                output += '\n'
                f.write(output)


def plot_bathymetry(b, ax=None, imgfile=None):
    """
    Plots bathymetry
    """
    lon = b.lon
    lat = b.lat
    nlon = len(lon)
    nlat = len(lat)
    dx_lon = numpy.diff(lon).mean()
    dx_lat = numpy.diff(lat).mean()
    lon_plot = numpy.linspace(lon[0] - dx_lon/2, lon[-1] + dx_lon/2, nlon + 1)
    lat_plot = numpy.linspace(lat[0] - dx_lat/2, lat[-1] + dx_lat/2, nlat + 1)

    if ax is None:
        ax = plt.subplot(111)
    dep = b.depth.filled(numpy.nan)
    p = ax.pcolormesh(lon_plot, lat_plot, dep.T)
    ax.set_xlabel('Longitude [deg E]')
    ax.set_ylabel('Latitude [deg N]')
    plt.colorbar(p, ax=ax, label='Depth [m]')

    if imgfile is None:
        plt.show()
    else:
        print('Saving image {:}'.format(imgfile))
        plt.savefig(imgfile, dpi=200, bbox_inches='tight')
        plt.close()
