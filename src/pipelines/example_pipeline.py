"""
Example Apache Beam Pipeline

A simple example pipeline that demonstrates basic Apache Beam concepts
and can be run locally or on Google Cloud Dataflow.
"""

import apache_beam as beam
import logging
from typing import List, Tuple

def run_pipeline(
    pipeline_args: List[str] = None,
    input_data: List[int] = None
) -> None:
    """
    Run the example pipeline.
    
    Args:
        pipeline_args: Command line arguments for the pipeline
        input_data: Sample input data (if None, uses default data)
    """
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    
    # Default input data if none provided
    if input_data is None:
        input_data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    
    # Create the pipeline
    with beam.Pipeline(argv=pipeline_args) as pipeline:
        # Create PCollection from input data
        numbers = (
            pipeline
            | 'Create numbers' >> beam.Create(input_data)
            | 'Log input' >> beam.Map(lambda x: logger.info(f'Input: {x}') or x)
        )
        
        # Transform the data
        transformed = (
            numbers
            | 'Multiply by 2' >> beam.Map(lambda x: x * 2)
            | 'Filter even numbers' >> beam.Filter(lambda x: x % 2 == 0)
            | 'Add index' >> beam.Map(lambda x: (x, f'number_{x}'))
        )
        
        # Output the results
        (
            transformed
            | 'Log output' >> beam.Map(lambda x: logger.info(f'Output: {x}') or x)
            | 'Write to console' >> beam.Map(print)
        )

def main():
    """Main entry point for the pipeline."""
    import sys
    
    # Basic pipeline arguments
    pipeline_args = sys.argv[1:]
    
    # Run the pipeline
    run_pipeline(pipeline_args)

if __name__ == '__main__':
    main()
