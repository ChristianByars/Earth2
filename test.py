import xarray as xr

ds = xr.open_zarr("gs://weatherbench2/datasets/era5/1959-2023_01_10-wb13-6h-1440x721.zarr")
print("vars:", list(ds.data_vars)[:40], "...")
print("lat shape:", ds.latitude.shape, "lon shape:", ds.longitude.shape)
print("levels:", ds.level.values if "level" in ds.coords else "no level coord")
