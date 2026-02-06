"""
Tests for pipeline utility functions.
"""

import unittest
from unittest.mock import patch, MagicMock
import apache_beam as beam
from apache_beam.testing.test_pipeline import TestPipeline
from apache_beam.testing.util import assert_that, equal_to

from pipelines.utils import (
    parse_csv_row,
    format_output,
    add_timestamp,
    ValidateSchema,
    FilterInvalidRecords,
    LogElement
)


class TestUtils(unittest.TestCase):
    """Test cases for utility functions."""
    
    def test_parse_csv_row(self):
        """Test CSV parsing function."""
        # Test normal case
        result = parse_csv_row("field1,field2,field3")
        expected_key = "field1"
        expected_dict = {
            "field_0": "field1",
            "field_1": "field2", 
            "field_2": "field3"
        }
        self.assertEqual(result[0], expected_key)
        self.assertEqual(result[1], expected_dict)
        
        # Test empty row
        result = parse_csv_row("")
        self.assertEqual(result[0], "")
        self.assertEqual(result[1], {})
        
        # Test single field
        result = parse_csv_row("single")
        self.assertEqual(result[0], "single")
        self.assertEqual(result[1], {"field_0": "single"})
    
    def test_parse_csv_row_custom_delimiter(self):
        """Test CSV parsing with custom delimiter."""
        result = parse_csv_row("field1|field2|field3", delimiter="|")
        expected_dict = {
            "field_0": "field1",
            "field_1": "field2",
            "field_2": "field3"
        }
        self.assertEqual(result[1], expected_dict)
    
    def test_format_output(self):
        """Test output formatting function."""
        # Test normal tuple
        result = format_output(("key1", "value1"))
        self.assertEqual(result, "Key: key1, Value: value1")
        
        # Test with different value types
        result = format_output(("key2", {"nested": "data"}))
        self.assertEqual(result, "Key: key2, Value: {'nested': 'data'}")
    
    def test_add_timestamp(self):
        """Test timestamp addition."""
        element = "test_element"
        timestamped = add_timestamp(element)
        
        self.assertIsInstance(timestamped, beam.window.TimestampedValue)
        self.assertEqual(timestamped.value, element)
        self.assertIsInstance(timestamped.timestamp, int)
    
    def test_filter_invalid_records(self):
        """Test invalid record filtering."""
        filter_fn = FilterInvalidRecords()
        
        # Test with valid records
        valid_records = ["valid1", "valid2", None, "valid3"]
        with TestPipeline() as pipeline:
            input_pcoll = pipeline | beam.Create(valid_records)
            output = input_pcoll | beam.ParDo(filter_fn)
            
            assert_that(output, equal_to(["valid1", "valid2", "valid3"]))
    
    @patch('pipelines.utils.logger')
    def test_log_element(self, mock_logger):
        """Test element logging."""
        log_fn = LogElement(prefix="Test")
        
        # Test logging functionality
        list(log_fn.process("test_element"))
        
        # Verify logger was called
        mock_logger.info.assert_called_once_with("Test: test_element")
    
    def test_validate_schema(self):
        """Test schema validation."""
        required_fields = ["id", "name"]
        validate_fn = ValidateSchema(required_fields)
        
        # Test valid records
        valid_record = {"id": 1, "name": "test", "extra": "field"}
        invalid_record = {"id": 1}  # Missing 'name' field
        non_dict_record = "not a dict"
        
        with TestPipeline() as pipeline:
            input_pcoll = pipeline | beam.Create([valid_record, invalid_record, non_dict_record])
            output = input_pcoll | beam.ParDo(validate_fn)
            
            assert_that(output, equal_to([valid_record]))


if __name__ == '__main__':
    unittest.main()
