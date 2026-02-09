"""
MySQL to BigQuery Dataflow Pipeline

An Apache Beam pipeline that reads data from MySQL database
and loads it into BigQuery using Google Cloud Dataflow.
"""

import apache_beam as beam
import logging
import json
from typing import List, Dict, Any, Optional
from apache_beam.options.pipeline_options import PipelineOptions, StandardOptions, GoogleCloudOptions, SetupOptions
from apache_beam.io.jdbc import ReadFromJdbc
from apache_beam.io import WriteToBigQuery

class MySQLToBigQueryOptions(PipelineOptions):
    """
    Custom pipeline options for MySQL to BigQuery pipeline.
    """
    @classmethod
    def _add_argparse_args(cls, parser):
        # MySQL Configuration
        parser.add_argument(
            '--mysql_host',
            type=str,
            default='localhost',
            help='MySQL host address'
        )
        parser.add_argument(
            '--mysql_port',
            type=int,
            default=3306,
            help='MySQL port'
        )
        parser.add_argument(
            '--mysql_database',
            type=str,
            required=True,
            help='MySQL database name'
        )
        parser.add_argument(
            '--mysql_table',
            type=str,
            required=True,
            help='MySQL table name'
        )
        parser.add_argument(
            '--mysql_username',
            type=str,
            required=True,
            help='MySQL username'
        )
        parser.add_argument(
            '--mysql_password',
            type=str,
            required=True,
            help='MySQL password'
        )
        
        # BigQuery Configuration
        parser.add_argument(
            '--bigquery_table',
            type=str,
            required=True,
            help='BigQuery table name (project:dataset.table)'
        )
        parser.add_argument(
            '--bigquery_schema',
            type=str,
            help='BigQuery schema as JSON string or file path'
        )
        
        # Data Processing Options
        parser.add_argument(
            '--batch_size',
            type=int,
            default=10000,
            help='Batch size for reading from MySQL'
        )
        parser.add_argument(
            '--query',
            type=str,
            help='Custom SQL query (overrides table reading)'
        )

class MySQLRowToDict(beam.DoFn):
    """Convert MySQL Row objects to dictionaries."""
    
    def process(self, row):
        try:
            # Convert row to dictionary using column names
            if hasattr(row, '_fields'):
                # For named tuples
                yield dict(zip(row._fields, row))
            else:
                # For regular tuples, use indices
                yield {f'col_{i}': val for i, val in enumerate(row)}
        except Exception as e:
            logging.warning(f"Failed to convert row to dict: {e}")
            yield {}

class TransformForBigQuery(beam.DoFn):
    """Transform data for BigQuery compatibility."""
    
    def process(self, element: Dict[str, Any]):
        try:
            transformed = {}
            for key, value in element.items():
                # Clean column names
                clean_key = str(key).lower().replace(' ', '_').replace('-', '_')
                
                # Handle None values
                if value is None:
                    transformed[clean_key] = None
                # Handle datetime objects
                elif hasattr(value, 'strftime'):
                    transformed[clean_key] = value.isoformat()
                # Handle other types
                else:
                    transformed[clean_key] = value
            
            yield transformed
        except Exception as e:
            logging.warning(f"Failed to transform element: {e}")
            yield {}

def infer_bigquery_schema(sample_data: List[Dict[str, Any]]) -> str:
    """
    Infer BigQuery schema from sample data.
    
    Args:
        sample_data: Sample records for schema inference
        
    Returns:
        BigQuery schema as JSON string
    """
    if not sample_data:
        return "[]"
    
    schema_fields = []
    
    # Get all possible keys from sample data
    all_keys = set()
    for record in sample_data:
        all_keys.update(record.keys())
    
    for key in sorted(all_keys):
        values = [record.get(key) for record in sample_data if record.get(key) is not None]
        
        if not values:
            bq_type = "STRING"
        else:
            sample_value = values[0]
            
            if isinstance(sample_value, bool):
                bq_type = "BOOLEAN"
            elif isinstance(sample_value, int):
                bq_type = "INTEGER"
            elif isinstance(sample_value, float):
                bq_type = "FLOAT"
            elif isinstance(sample_value, str):
                bq_type = "STRING"
            else:
                bq_type = "STRING"
        
        schema_fields.append({
            "name": key,
            "type": bq_type,
            "mode": "NULLABLE"
        })
    
    return json.dumps(schema_fields)

def run_mysql_to_bigquery_pipeline(options: MySQLToBigQueryOptions) -> None:
    """
    Run the MySQL to BigQuery pipeline.
    
    Args:
        options: Pipeline options containing all configuration
    """
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    
    # Validate required parameters
    if not all([options.mysql_database, options.mysql_table, 
                options.mysql_username, options.mysql_password,
                options.bigquery_table]):
        raise ValueError("Missing required parameters")
    
    # Build JDBC connection string
    jdbc_url = f"jdbc:mysql://{options.mysql_host}:{options.mysql_port}/{options.mysql_database}"
    
    # Build JDBC properties
    jdbc_properties = {
        "user": options.mysql_username,
        "password": options.mysql_password,
        "driver": "com.mysql.cj.jdbc.Driver"
    }
    
    logger.info(f"Connecting to MySQL: {options.mysql_host}:{options.mysql_port}/{options.mysql_database}")
    logger.info(f"Reading from table: {options.mysql_table}")
    logger.info(f"Writing to BigQuery: {options.bigquery_table}")
    
    # Create the pipeline
    with beam.Pipeline(options=options) as pipeline:
        # Read from MySQL
        mysql_data = (
            pipeline
            | 'Read from MySQL' >> ReadFromJdbc(
                table_name=options.mysql_table,
                driver_class_name="com.mysql.cj.jdbc.Driver",
                jdbc_url=jdbc_url,
                username=options.mysql_username,
                password=options.mysql_password,
                query=options.query if options.query else None
            )
        )
        
        # Convert rows to dictionaries
        dict_data = (
            mysql_data
            | 'Convert to Dict' >> beam.ParDo(MySQLRowToDict())
        )
        
        # Transform for BigQuery compatibility
        transformed_data = (
            dict_data
            | 'Transform for BigQuery' >> beam.ParDo(TransformForBigQuery())
        )
        
        # Sample data for schema inference (if schema not provided)
        if not options.bigquery_schema:
            sample_data = (
                transformed_data
                | 'Sample Data' >> beam.combiners.Sample.FixedSizeGlobally(10)
                | 'Flatten Sample' >> beam.FlatMap(lambda x: x)
            )
            
            schema = (
                sample_data
                | 'Infer Schema' >> beam.Map(lambda data: infer_bigquery_schema(data))
                | 'Get Schema' >> beam.combiners.ToList()
            )
            
            # Use the inferred schema for BigQuery write
            bigquery_schema = schema
        else:
            # Use provided schema
            if options.bigquery_schema.startswith('{'):
                # Direct JSON string
                bigquery_schema = beam.Create([options.bigquery_schema])
            else:
                # File path
                bigquery_schema = (
                    pipeline
                    | 'Read Schema File' >> beam.io.ReadFromText(options.bigquery_schema)
                    | 'Parse Schema' >> beam.Map(lambda x: x.strip())
                )
        
        # Write to BigQuery
        (
            transformed_data
            | 'Write to BigQuery' >> WriteToBigQuery(
                table=options.bigquery_table,
                schema=bigquery_schema,
                write_disposition=beam.io.BigQueryDisposition.WRITE_TRUNCATE,
                create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED,
                custom_gcs_temp_location=f"gs://temp-{options.mysql_database}/"
            )
        )

def main():
    """Main entry point for the pipeline."""
    import sys
    
    # Create pipeline options
    options = PipelineOptions(sys.argv[1:])
    custom_options = options.view_as(MySQLToBigQueryOptions)
    
    # Set Dataflow runner
    if not hasattr(options.view_as(StandardOptions), 'runner'):
        options.view_as(StandardOptions).runner = 'DataflowRunner'
    
    # Set up Google Cloud options
    google_cloud_options = options.view_as(GoogleCloudOptions)
    if not google_cloud_options.project:
        raise ValueError("GCP project must be specified")
    
    # Save main session
    options.view_as(SetupOptions).save_main_session = True
    
    try:
        run_mysql_to_bigquery_pipeline(custom_options)
    except Exception as e:
        logging.error(f"Pipeline failed: {e}")
        raise 

if __name__ == '__main__':
    main()
