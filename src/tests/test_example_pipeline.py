"""
Tests for the example pipeline.
"""

import unittest
from unittest.mock import patch, MagicMock
import apache_beam as beam
from apache_beam.testing.test_pipeline import TestPipeline
from apache_beam.testing.util import assert_that, equal_to

from pipelines.example_pipeline import run_pipeline


class TestExamplePipeline(unittest.TestCase):
    """Test cases for the example pipeline."""
    
    def test_pipeline_local_execution(self):
        """Test pipeline execution with DirectRunner."""
        # Test data
        input_data = [1, 2, 3, 4, 5]
        expected_output = [4, 8, 12, 16, 20]  # Even numbers multiplied by 2
        
        with TestPipeline() as pipeline:
            # Create PCollection
            input_pcoll = pipeline | beam.Create(input_data)
            
            # Apply transformations (simplified version of pipeline)
            output = (
                input_pcoll
                | beam.Map(lambda x: x * 2)
                | beam.Filter(lambda x: x % 2 == 0)
            )
            
            # Assert results
            assert_that(output, equal_to(expected_output))
    
    def test_pipeline_with_empty_input(self):
        """Test pipeline behavior with empty input."""
        with TestPipeline() as pipeline:
            input_pcoll = pipeline | beam.Create([])
            
            output = (
                input_pcoll
                | beam.Map(lambda x: x * 2)
                | beam.Filter(lambda x: x % 2 == 0)
            )
            
            assert_that(output, equal_to([]))
    
    def test_pipeline_with_negative_numbers(self):
        """Test pipeline with negative numbers."""
        input_data = [-3, -2, -1, 0, 1, 2, 3]
        expected_output = [-4, 0, 4]  # Even numbers multiplied by 2
        
        with TestPipeline() as pipeline:
            input_pcoll = pipeline | beam.Create(input_data)
            
            output = (
                input_pcoll
                | beam.Map(lambda x: x * 2)
                | beam.Filter(lambda x: x % 2 == 0)
            )
            
            assert_that(output, equal_to(expected_output))
    
    @patch('pipelines.example_pipeline.logging.getLogger')
    def test_pipeline_logging(self, mock_get_logger):
        """Test that pipeline logging works correctly."""
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger
        
        # This test verifies that logging is called
        # In a real scenario, you might capture log output
        run_pipeline(input_data=[1, 2, 3])
        
        # Verify logger was called
        mock_get_logger.assert_called_once()


if __name__ == '__main__':
    unittest.main()
