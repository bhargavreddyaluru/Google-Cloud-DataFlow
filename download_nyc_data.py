"""
Bulk download NYC taxi data for 100GB dataset
"""

import os
import requests
from datetime import datetime, timedelta

def download_nyc_taxi_data(years=[2022, 2023], months=None):
    """
    Download NYC taxi data for specified years and months.
    
    Args:
        years: List of years to download
        months: List of months to download (1-12), default all months
    """
    if months is None:
        months = list(range(1, 13))
    
    base_url = "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_{year}-{month:02d}.parquet"
    
    total_files = len(years) * len(months)
    downloaded = 0
    
    print(f"Starting download of {total_files} files...")
    print(f"Estimated total size: ~{total_files * 50}MB")
    
    for year in years:
        for month in months:
            url = base_url.format(year=year, month=month)
            filename = f"yellow_tripdata_{year}-{month:02d}.parquet"
            
            if os.path.exists(filename):
                print(f"Skipping {filename} (already exists)")
                downloaded += 1
                continue
            
            print(f"Downloading {filename}...")
            
            try:
                # Use requests to download the file
                response = requests.get(url, stream=True)
                response.raise_for_status()
                
                with open(filename, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                
                downloaded += 1
                file_size = os.path.getsize(filename) / (1024*1024)
                print(f"✓ Downloaded {filename} ({file_size:.1f}MB) ({downloaded}/{total_files})")
                
            except Exception as e:
                print(f"✗ Error downloading {filename}: {e}")
    
    print(f"\nDownload complete: {downloaded}/{total_files} files")
    
    # Calculate total size
    total_size = 0
    for year in years:
        for month in months:
            filename = f"yellow_tripdata_{year}-{month:02d}.parquet"
            if os.path.exists(filename):
                total_size += os.path.getsize(filename)
    
    print(f"Total downloaded size: {total_size / (1024**3):.2f} GB")

if __name__ == '__main__':
    # Download 2 years of data (24 files = ~1.2GB)
    # For 100GB, you'd need about 200+ files (8+ years)
    download_nyc_taxi_data(years=[2022, 2023])
    
    print("\nFor 100GB dataset, uncomment the line below:")
    print("# download_nyc_taxi_data(years=[2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023])")
