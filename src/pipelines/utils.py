"""
Pipeline Utility Functions

Common utility functions for Apache Beam pipelines.
"""

import apache_beam as beam
from typing import Any, Dict, List, Tuple
import logging

logger = logging.getLogger(__name__)

class LogElement(beam.DoFn):
    """A DoFn that logs elements for debugging."""
    
    def __init__(self, prefix: str = "Element"):
        self.prefix = prefix
    
    def process(self, element: Any):
        logger.info(f"{self.prefix}: {element}")
        yield element

class FilterInvalidRecords(beam.DoFn):
    """Filter out invalid or None records."""
    
    def process(self, element: Any):
        if element is not None:
            yield element

def parse_csv_row(row: str, delimiter: str = ",") -> Tuple[str, Dict[str, str]]:
    """
    Parse a CSV row into a tuple of (row_key, parsed_dict).
    
    Args:
        row: CSV string to parse
        delimiter: CSV delimiter character
        
    Returns:
        Tuple of (row_key, parsed_dict)
    """
    try:
        fields = row.split(delimiter)
        # Use first field as key, rest as values
        row_key = fields[0] if fields else ""
        parsed_dict = {f"field_{i}": field for i, field in enumerate(fields)}
        return row_key, parsed_dict
    except Exception as e:
        logger.error(f"Error parsing CSV row '{row}': {e}")
        return "", {}

def format_output(element: Tuple[Any, Any]) -> str:
    """
    Format pipeline output as a string.
    
    Args:
        element: Tuple to format
        
    Returns:
        Formatted string
    """
    try:
        key, value = element
        return f"Key: {key}, Value: {value}"
    except Exception as e:
        logger.error(f"Error formatting element {element}: {e}")
        return f"Invalid element: {element}"

def add_timestamp(element: Any) -> beam.window.TimestampedValue:
    """
    Add current timestamp to element for windowing operations.
    
    Args:
        element: Element to timestamp
        
    Returns:
        TimestampedValue with current timestamp
    """
    import time
    return beam.window.TimestampedValue(element, int(time.time()))

class ValidateSchema(beam.DoFn):
    """
    Validate that elements conform to expected schema.
    """
    
    def __init__(self, required_fields: List[str]):
        self.required_fields = required_fields
    
    def process(self, element: Dict[str, Any]):
        if isinstance(element, dict):
            missing_fields = [field for field in self.required_fields if field not in element]
            if not missing_fields:
                yield element
            else:
                logger.warning(f"Missing required fields {missing_fields} in element: {element}")
        else:
            logger.warning(f"Element is not a dictionary: {element}")

def create_window_strategy(
    window_size: int = 60,
    allowed_lateness: int = 300
) -> beam.WindowFn:
    """
    Create a fixed window strategy for streaming pipelines.
    
    Args:
        window_size: Window size in seconds
        allowed_lateness: Allowed lateness in seconds
        
    Returns:
        WindowFn object
    """
    return beam.window.FixedWindows(window_size, allowed_lateness=allowed_lateness)
