# GCS to BigQuery Dataflow Pipeline

This Apache Beam pipeline reads CSV files from Google Cloud Storage (GCS) and loads the data into BigQuery using Google Cloud Dataflow.

## Prerequisites

1. **Google Cloud Project**: Set up a GCP project with billing enabled
2. **APIs Enabled**: Enable the following APIs:
   - Dataflow API
   - BigQuery API
   - Cloud Storage API
   - Cloud Build API

3. **Service Account**: Create a service account with the following roles:
   - Dataflow Admin
   - BigQuery Data Editor
   - Storage Object Admin

4. **Authentication**: Set up authentication:
   ```bash
   gcloud auth application-default login
   # OR use service account key
   export GOOGLE_APPLICATION_CREDENTIALS="path/to/service-account-key.json"
   ```

## Installation

1. **Install dependencies**:
   ```bash
   pip install -r requirements-gcp.txt
   ```

2. **Set up environment**:
   ```bash
   cp .env.example .env
   # Edit .env with your actual values
   ```

## Configuration

Update the `.env` file with your actual values:

```bash
# Google Cloud Configuration
GOOGLE_CLOUD_PROJECT=your-actual-project-id
GOOGLE_CLOUD_REGION=us-central1

# GCS Configuration
GCS_BUCKET=your-actual-bucket-name
GCS_INPUT_PATH=gs://your-actual-bucket-name/input/*.csv

# BigQuery Configuration
BQ_DATASET=your_actual_dataset
BQ_TABLE=your_actual_table
BQ_TABLE_FULL=your-actual-project-id:your_actual_dataset.your_actual_table

# CSV Headers (match your CSV structure)
CSV_HEADERS=id,name,email,age
```

## Usage

### 1. Local Testing (DirectRunner)

```bash
python src/pipelines/gcs_to_bigquery_pipeline.py \
  --runner=DirectRunner \
  --gcs_input_path=gs://your-bucket/input/*.csv \
  --bigquery_table=your-project:your_dataset.your_table \
  --csv_headers=id,name,email,age \
  --project=your-project
```

### 2. Dataflow Deployment (DataflowRunner)

```bash
python src/pipelines/gcs_to_bigquery_pipeline.py \
  --runner=DataflowRunner \
  --project=your-project-id \
  --region=us-central1 \
  --staging_location=gs://your-bucket/staging \
  --temp_location=gs://your-bucket/temp \
  --gcs_input_path=gs://your-bucket/input/*.csv \
  --bigquery_table=your-project:your_dataset.your_table \
  --csv_headers=id,name,email,age \
  --job_name=gcs-to-bq-$(date +%Y%m%d-%H%M%S)
```

### 3. Using Environment Variables

```bash
# Set environment variables
export GOOGLE_CLOUD_PROJECT=your-project-id
export GCS_INPUT_PATH=gs://your-bucket/input/*.csv
export BQ_TABLE_FULL=your-project:your_dataset.your_table

# Run pipeline
python src/pipelines/gcs_to_bigquery_pipeline.py \
  --runner=DataflowRunner \
  --region=us-central1 \
  --staging_location=gs://your-bucket/staging \
  --temp_location=gs://your-bucket/temp
```

## Pipeline Components

### 1. Read from GCS
- Reads CSV files from the specified GCS path
- Supports wildcards for multiple files
- Skips header rows automatically

### 2. Parse CSV
- Converts CSV lines to dictionaries
- Uses specified headers as keys
- Handles parsing errors gracefully

### 3. Write to BigQuery
- Creates table if it doesn't exist
- Supports both append and truncate modes
- Auto-generates schema from CSV headers

## Customization

### Custom CSV Headers
Update the `CSV_HEADERS` in your `.env` file or pass via command line:

```bash
--csv_headers=col1,col2,col3,col4
```

### Custom Schema
Modify the pipeline to use custom BigQuery schema:

```python
# In the pipeline, replace the auto-generated schema:
custom_schema = "id:INTEGER,name:STRING,email:STRING,age:INTEGER"

| 'Write to BigQuery' >> beam.io.WriteToBigQuery(
    table=bigquery_table,
    schema=custom_schema,
    # ... other options
)
```

### Data Transformation
Add custom transformations between parsing and writing:

```python
transformed_data = (
    parsed_data
    | 'Transform Data' >> beam.Map(lambda x: {
        **x,
        'age': int(x['age']),  # Convert to integer
        'processed_timestamp': datetime.now().isoformat()
    })
)
```

## Monitoring

1. **Dataflow Console**: Monitor job progress at
   `https://console.cloud.google.com/dataflow`

2. **BigQuery Console**: Check data at
   `https://console.cloud.google.com/bigquery`

3. **Cloud Storage**: Verify input files and temporary files

## Troubleshooting

### Common Issues

1. **Permission Errors**: Ensure service account has proper permissions
2. **Schema Mismatch**: Check that CSV headers match BigQuery table schema
3. **File Not Found**: Verify GCS path and file existence
4. **Quota Issues**: Check Dataflow and BigQuery quotas

### Debug Mode

Run with additional logging:

```bash
python src/pipelines/gcs_to_bigquery_pipeline.py \
  --runner=DirectRunner \
  --gcs_input_path=gs://your-bucket/input/*.csv \
  --bigquery_table=your-project:your_dataset.your_table \
  --csv_headers=id,name,email,age \
  --project=your-project \
  --log_level=DEBUG
```

## Cost Optimization

1. **Use appropriate machine types** for your data size
2. **Clean up temporary files** in GCS after job completion
3. **Consider partitioning** large tables by date
4. **Use streaming inserts** for real-time needs

## Example Data

Use the provided `sample_data.csv` to test the pipeline:

```bash
# Upload sample data to GCS
gsutil cp sample_data.csv gs://your-bucket/input/

# Run pipeline
python src/pipelines/gcs_to_bigquery_pipeline.py \
  --runner=DataflowRunner \
  --project=your-project-id \
  --region=us-central1 \
  --staging_location=gs://your-bucket/staging \
  --temp_location=gs://your-bucket/temp \
  --gcs_input_path=gs://your-bucket/input/sample_data.csv \
  --bigquery_table=your-project:your_dataset.your_table \
  --csv_headers=id,name,email,age
```
