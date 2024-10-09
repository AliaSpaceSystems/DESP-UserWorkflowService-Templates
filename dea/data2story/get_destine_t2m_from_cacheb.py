import xarray as xr

# output filename
filename = 't2m_destine_20240801.nc'

# retrieve destine single level data from cacheb. Dataset of interest: t2m (t metre temperature)
data = xr.open_dataset(
        "https://cacheb.dcms.destine.eu/d1-climate-dt/ScenarioMIP-SSP3-7.0-IFS-NEMO-0001-high-sfc-v0.zarr",
        engine="zarr",
        storage_options={"client_kwargs": {"trust_env": "true"}},
        chunks={},
    )
print(data)
# Convert to Celsius

t2m = data.t2m.astype("float32") - 273.15
t2m.attrs["units"] = "C"

t2m = t2m.assign_coords(longitude=(t2m['longitude'] % 360))  # First ensure longitude is in 0-360 range
t2m['longitude'] = xr.where(t2m['longitude'] > 180, t2m['longitude'] - 360, t2m['longitude'])  # Then shift to -180 to 180

# Sort by longitude to maintain the proper order
t2m = t2m.sortby('longitude')

# t2m['longitude'] = xr.where(t2m['longitude'] > 180, t2m['longitude'] - 360, t2m['longitude'])



# get a single time step
t2m_slice = t2m.sel(valid_time="2024-08-01T12:00:00")

print(f"Data to download...")
print(t2m_slice)

t2m_slice = t2m_slice.compute()
# save as NetCDF
t2m_slice.to_netcdf(filename)

print(f"Your file {filename} is ready!")
