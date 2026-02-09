"""
Convert NYC Taxi Parquet data to CSV for MySQL import
"""

import pandas as pd
import os
from pathlib import Path

def convert_parquet_to_csv(parquet_file: str, output_csv: str = None):
    """
    Convert Parquet file to CSV format suitable for MySQL import.
    
    Args:
        parquet_file: Path to parquet file
        output_csv: Output CSV file path (optional)
    """
    if output_csv is None:
        output_csv = parquet_file.replace('.parquet', '.csv')
    
    print(f"Reading parquet file: {parquet_file}")
    
    # Read parquet file in chunks to handle large files
    chunk_size = 100000  # 100k rows at a time
    
    try:
        # First, get the schema and sample data
        df_sample = pd.read_parquet(parquet_file)
        df_sample = df_sample.head(1000)  # Take first 1000 rows as sample
        print(f"Columns found: {list(df_sample.columns)}")
        print(f"Sample data shape: {df_sample.shape}")
        print(f"Data types:\n{df_sample.dtypes}")
        
        # Read full data
        print("Reading full dataset...")
        df = pd.read_parquet(parquet_file)
        
        print(f"Full dataset shape: {df.shape}")
        
        # Clean column names for MySQL
        df.columns = [col.replace(' ', '_').replace('-', '_').lower() for col in df.columns]
        
        # Handle missing values
        df = df.fillna('')
        
        # Convert datetime columns
        for col in df.columns:
            if 'datetime' in col or 'time' in col:
                df[col] = pd.to_datetime(df[col], errors='coerce')
        
        print(f"Cleaned columns: {list(df.columns)}")
        
        # Write to CSV
        print(f"Writing to CSV: {output_csv}")
        df.to_csv(output_csv, index=False, encoding='utf-8')
        
        print(f"CSV file created: {output_csv}")
        print(f"CSV file size: {os.path.getsize(output_csv) / (1024*1024):.2f} MB")
        
        return output_csv
        
    except Exception as e:
        print(f"Error converting parquet to CSV: {e}")
        return None

def generate_mysql_create_table(csv_file: str, table_name: str = 'nyc_taxi_trips'):
    """
    Generate MySQL CREATE TABLE statement based on CSV data.
    
    Args:
        csv_file: Path to CSV file
        table_name: MySQL table name
    """
    try:
        # Read first few rows to infer schema
        df_sample = pd.read_csv(csv_file, nrows=100)
        
        print(f"\nGenerating MySQL CREATE TABLE for {table_name}")
        print(f"Columns: {list(df_sample.columns)}")
        
        # Generate CREATE TABLE statement
        create_sql = f"CREATE TABLE {table_name} (\n"
        
        for col in df_sample.columns:
            dtype = df_sample[col].dtype
            
            if 'datetime' in col.lower() or 'time' in col.lower():
                mysql_type = 'DATETIME'
            elif dtype == 'int64':
                mysql_type = 'BIGINT'
            elif dtype == 'float64':
                mysql_type = 'DECIMAL(10,2)'
            else:
                mysql_type = 'TEXT'
            
            create_sql += f"    `{col}` {mysql_type},\n"
        
        create_sql = create_sql.rstrip(',\n') + "\n) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;"
        
        print(f"\nMySQL CREATE TABLE statement:\n{create_sql}")
        
        # Save to file
        sql_file = csv_file.replace('.csv', '_create_table.sql')
        with open(sql_file, 'w') as f:
            f.write(create_sql)
        
        print(f"SQL file saved: {sql_file}")
        
        return create_sql
        
    except Exception as e:
        print(f"Error generating MySQL schema: {e}")
        return None

if __name__ == '__main__':
    # Convert the downloaded parquet file
    parquet_file = 'yellow_tripdata_2023-01.parquet'
    
    if os.path.exists(parquet_file):
        # Convert to CSV
        csv_file = convert_parquet_to_csv(parquet_file)
        
        if csv_file:
            # Generate MySQL schema
            generate_mysql_create_table(csv_file)
            
            print(f"\nNext steps:")
            print(f"1. Upload CSV to Cloud Storage: gsutil cp {csv_file} gs://your-bucket/")
            print(f"2. Import to Cloud SQL using MySQL import tool")
            print(f"3. Create Dataflow template for Cloud SQL to BigQuery")
    else:
        print(f"Parquet file not found: {parquet_file}")
        print("Please download the file first using:")
        print("wget https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2023-01.parquet")
