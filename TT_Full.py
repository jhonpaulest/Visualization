from netCDF4 import Dataset
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.cm import get_cmap
import cartopy.crs as crs
from cartopy.feature import ShapelyFeature
import cartopy.io.shapereader as shpreader
from wrf import (getvar, interplevel, to_np, latlon_coords, get_cartopy,
                 cartopy_xlim, cartopy_ylim)
from datetime import datetime, timedelta
import os

# Buat direktori jika belum ada
output_dir = r'E:\STMKG\Semester7\Praktik_PCLN\UTS\WRF-NEW\tt'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Buka file NetCDF
ncfile = Dataset(r'E:\STMKG\Semester7\Praktik_PCLN\UTS\WRF-NEW\wrfout_d03_20230223_120000.nc')

# Dapatkan jumlah timesteps
num_times = len(ncfile.dimensions['Time'])

# Loop untuk setiap timestep
for timeidx in range(num_times):
    print(f"Processing timestep {timeidx + 1} of {num_times}")
    
    # Dapatkan waktu
    current_time = ncfile.variables['Times'][timeidx].tobytes().decode().strip()
    current_datetime = datetime.strptime(current_time, '%Y-%m-%d_%H:%M:%S')
    
    # Ekstrak variabel yang dibutuhkan
    p = getvar(ncfile, "pressure", timeidx)
    temp = getvar(ncfile, "temp", timeidx, units="degC")
    td = getvar(ncfile, "td", timeidx, units="degC")
    
    # Interpolasi ke level tekanan
    t850 = interplevel(temp, p, 850)
    t500 = interplevel(temp, p, 500)
    td850 = interplevel(td, p, 850)
    
    # Hitung Total Totals Index
    tt = t850 + td850 - 2*t500
    
    # Get the lat/lon coordinates
    lats, lons = latlon_coords(t850)
    
    # Get the map projection information
    cart_proj = get_cartopy(t850)
    
    # Create the figure
    fig = plt.figure(figsize=(12,9))
    ax = plt.axes(projection=cart_proj)
    
    # Load and add Indonesia shapefile
    shapefile = r'E:\STMKG\Semester7\Praktik_PCLN\SHP\SHP_Indonesia_kabupaten\INDONESIA_KAB.shp'
    shape_feature = ShapelyFeature(shpreader.Reader(shapefile).geometries(),
                                  crs.PlateCarree(), facecolor='none',
                                  edgecolor='black', linewidth=0.5)
    ax.add_feature(shape_feature)
    
    # Buat kontur untuk Total Totals Index
    levels = np.arange(38, 49, 1)
    tt_contours = plt.contourf(lons, lats, tt,
                              levels=levels,
                              cmap=get_cmap("jet"),
                              transform=crs.PlateCarree())
    
    # Tambahkan colorbar
    cbar = plt.colorbar(tt_contours, ax=ax, orientation="vertical", pad=.02)
    cbar.set_label('TT (°C)', fontsize=10)
    cbar.set_ticks(np.arange(38, 49, 1))
    
    # Set the map bounds
    ax.set_extent([106.5, 107.2, -6.5, -5.85], crs=crs.PlateCarree())
    
    # Set title dengan waktu
    title_time = current_datetime.strftime('%HUTC %d-%m-%Y')
    plt.title(f"TT {title_time}", pad=7, fontsize=15)
    
    # Simpan gambar
    output_filename = f'tt_{current_datetime.strftime("%Y%m%d_%H%M")}.png'
    output_path = os.path.join(output_dir, output_filename)
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()  # Tutup figure untuk menghemat memori

# Tutup file NetCDF
ncfile.close()

print("Selesai! Semua plot telah disimpan.")