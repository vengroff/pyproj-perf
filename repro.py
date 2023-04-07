"""Quick repro case of performance change from pyproj 3.4.1 to 3.5.0."""
import cProfile

import censusdis.data as ced
import pyproj
from censusdis.states import ALL_STATES_AND_DC

# Get all the counties in the 50 states and DC.
gdf_counties = ced.download(
    'acs/acs5', 2020, ['NAME'], state=ALL_STATES_AND_DC, county='*',
    with_geometry=True
)

print(f"pyproj.__version__ = {pyproj.__version__}")

cProfile.run("gdf_counties.to_crs(epsg=9311)", sort='time')
