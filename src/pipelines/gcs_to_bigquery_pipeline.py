"""
GCS to BigQuery Pipeline

An Apache Beam pipeline that reads CSV files from Google Cloud Storage
and loads the data into BigQuery using Google Cloud Dataflow.
"""

import apache_beam as beam
import logging
from typing import List, Dict, Any
from apache_beam.options.pipeline_options import PipelineOptions, StandardOptions, GoogleCloudOptions, SetupOptions

class ParseCSVFn(beam.DoFn):
    """Parse CSV lines into dictionaries."""
    
    def __init__(self, header: List[str]):
        self.header = header
    
    def process(self, element: str):
        try:
            values = element.strip().split(',')
            if len(values) == len(self.header):
                yield dict(zip(self.header, values))
        except Exception as e:
            logging.warning(f"Failed to parse CSV line: {element}. Error: {e}")

def run_pipeline(
    pipeline_args: List[str] = None,
    gcs_input_path: str = None,
    bigquery_table: str = None,
    csv_headers: List[str] = None
) -> None:
    """
    Run the GCS to BigQuery pipeline.
    
    Args:
        pipeline_args: Command line arguments for the pipeline
        gcs_input_path: GCS path to CSV file(s) (e.g., gs://bucket/path/*.csv)
        bigquery_table: BigQuery table name (e.g., project:dataset.table)
        csv_headers: List of CSV column headers
    """
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    
    # Default values if not provided
    if not gcs_input_path:
        gcs_input_path = "gs://your-bucket/input/*.csv"
    if not bigquery_table:
        bigquery_table = "your-project:your_dataset.your_table"
    if not csv_headers:
        csv_headers = ["id", "name", "email", "age"]  # Default headers
    
    # Set up pipeline options
    options = PipelineOptions(pipeline_args)
    google_cloud_options = options.view_as(GoogleCloudOptions)
    
    # Ensure we're running on Dataflow
    options.view_as(StandardOptions).runner = 'DataflowRunner'
    
    # Set up staging and temp locations
    if not google_cloud_options.staging_location:
        google_cloud_options.staging_location = "gs://your-bucket/staging"
    if not google_cloud_options.temp_location:
        google_cloud_options.temp_location = "gs://your-bucket/temp"
    
    # Project setup
    if not google_cloud_options.project:
        google_cloud_options.project = "your-gcp-project"
    
    # Save the main session
    options.view_as(SetupOptions).save_main_session = True
    
    # Create the pipeline
    with beam.Pipeline(options=options) as pipeline:
        # Read CSV files from GCS
        csv_lines = (
            pipeline
            | 'Read CSV from GCS' >> beam.io.ReadFromText(gcs_input_path, skip_header_lines=1)
        )
        
        # Parse CSV lines into dictionaries
        parsed_data = (
            csv_lines
            | 'Parse CSV' >> beam.ParDo(ParseCSVFn(csv_headers))
        )
        
        # Write to BigQuery
        (
            parsed_data
            | 'Write to BigQuery' >> beam.io.WriteToBigQuery(
                table=bigquery_table,
                schema=','.join([f"{header}:STRING" for header in csv_headers]),
                write_disposition=beam.io.BigQueryDisposition.WRITE_TRUNCATE,
                create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED,
                custom_gcs_temp_location=google_cloud_options.temp_location
            )
        )
        
        logger.info(f"Pipeline will read from: {gcs_input_path}")
        logger.info(f"Pipeline will write to: {bigquery_table}")

def main():
    """Main entry point for the pipeline."""
    import sys
    
    # Basic pipeline arguments
    pipeline_args = sys.argv[1:]
    
    # Example usage with command line arguments:
    # python gcs_to_bigquery_pipeline.py \
    #   --gcs_input_path=gs://my-bucket/data/*.csv \
    #   --bigquery_table=my-project:my_dataset.my_table \
    #   --csv_headers=id,name,email,age \
    #   --project=my-project \
    #   --region=us-central1 \
    #   --staging_location=gs://my-bucket/staging \
    #   --temp_location=gs://my-bucket/temp
    
    # Parse custom arguments
    gcs_input_path = None
    bigquery_table = None
    csv_headers = None
    
    for i, arg in enumerate(pipeline_args):
        if arg.startswith('--gcs_input_path='):
            gcs_input_path = arg.split('=', 1)[1]
        elif arg.startswith('--bigquery_table='):
            bigquery_table = arg.split('=', 1)[1]
        elif arg.startswith('--csv_headers='):
            csv_headers = arg.split('=', 1)[1].split(',')
    
    # Run the pipeline
    run_pipeline(pipeline_args, gcs_input_path, bigquery_table, csv_headers)

if __name__ == '__main__':
    main()
