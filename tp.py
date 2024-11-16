# Import library yang dibutuhkan
import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import pandas as pd
from cartopy.io.shapereader import Reader
from cartopy.feature import ShapelyFeature
import os

# Buat direktori jika belum ada
output_dir = r'E:\STMKG\Semester7\Praktik_PCLN\UTS\ERA5\tp'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Membaca file NetCDF
data = xr.open_dataset(r'E:\STMKG\Semester7\Praktik_PCLN\UTS\ERA5\era5_23022023_12-23z.nc')

# Memilih variabel CAPE
tp = data['tp']*1000

# Mendapatkan jumlah timesteps
num_times = len(data.valid_time)

# Loop untuk setiap timestep
for time_idx in range(num_times):
    print(f"Processing timestep {time_idx + 1} of {num_times}")
    
    # Memilih waktu yang diinginkan
    tp_time = tp.isel(valid_time=time_idx)
    
    # Mendapatkan waktu valid
    waktu_valid = data['valid_time'].isel(valid_time=time_idx).values
    waktu_valid_str = pd.to_datetime(waktu_valid).strftime('%H UTC %Y-%m-%d')
    
    # Membuat plot
    plt.figure(figsize=(3, 2))
    ax = plt.axes(projection=ccrs.PlateCarree())
    
    # Mengatur rentang latitude dan longitude
    lon_min, lon_max = 106.5, 107.2
    lat_min, lat_max = -6.5, -5.85
    ax.set_extent([lon_min, lon_max, lat_min, lat_max], crs=ccrs.PlateCarree())
    
    # Menambahkan shapefile Indonesia
    shapefile_path = r'E:\STMKG\Semester7\Praktik_PCLN\SHP\SHP_Indonesia_kabupaten\INDONESIA_KAB.shp'
    shape_feature = ShapelyFeature(Reader(shapefile_path).geometries(),
                                  ccrs.PlateCarree(),
                                  facecolor='none',
                                  edgecolor='black',
                                  linewidth=1)
    ax.add_feature(shape_feature)
    
    # Plot data CAPE
    im = tp_time.plot(ax=ax, 
                       cmap='turbo',
                       vmin=0.5,
                       vmax=7,
                       cbar_kwargs={'label': 'Total Presipitasi (mm)',
                                    'orientation': 'vertical',
                                    'pad': 0.02, 
                                    'ticks': [0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5, 6, 6.5, 7]})
    
    #add_colorbar=False)    
    #copy-paste jika ingin menggunakan cbar
    #cbar_kwargs={'label': 'Total Presipitasi (mm)',
    #             'orientation': 'vertical',
    #             'pad': 0.02, 
    #             'ticks': [0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5, 6, 6.5, 7]})

    # Mengatur ukuran font untuk label dan ticks colorbar
    cbar = im.colorbar
    cbar.ax.tick_params(labelsize=5)                      # Ukuran font ticks
    cbar.ax.xaxis.set_label_position('top')               # Menempatkan label di atas colorbar
    cbar.set_label('Total Presipitasi (mm)', fontsize=5)  # Ukuran font label
    cbar.ax.xaxis.labelpad = 1                            # Mengatur jarak label dari colorbar

    # Menambahkan gridlines
    gl = ax.gridlines(draw_labels=True, linestyle='--', alpha=0.5, linewidth=0)
    gl.top_labels = False    # Menyembunyikan label di bagian atas
    gl.right_labels = False  # Menyembunyikan label di sisi kanan

    # Mengatur ukuran font untuk label koordinat
    gl.xlabel_style = {'size': 5, 'weight': 'bold'}  # Ukuran font untuk label bujur (longitude)
    gl.ylabel_style = {'size': 5, 'weight': 'bold'}  # Ukuran font untuk label lintang (latitude)
    
    # Menambahkan judul
    plt.title(f'Total Presipitasi ERA5 {waktu_valid_str}', pad=3, fontsize=5, weight= 'bold')
    
    # Mengatur layout
    plt.tight_layout()
    
    # Menyimpan plot
    output_filename = f'tp_{pd.to_datetime(waktu_valid).strftime("%Y%m%d_%H%M")}.png'
    output_path = os.path.join(output_dir, output_filename)
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()  # Menutup figure untuk menghemat memori

print("Selesai! Semua plot telah disimpan.")