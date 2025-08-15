import pytest

from csv_processor import CSVProcessor
from csv_processor_simple import CSVProcessorSimple

@pytest.fixture
def csv_processor():
    return CSVProcessor("packages.csv")

@pytest.fixture
def csv_processor_simple():
    return CSVProcessorSimple("packages.csv")

def test_process_csv(csv_processor):
    csv_processor.process()
    assert False

def test_process_csv_simple(csv_processor_simple):
    csv_processor_simple.process()
    csv_processor_simple.print_statistics()
    assert False