import ocdsextensionregistry.validate
import os
import pytest


def test_ok():
    ocdsextensionregistry.validate.registry_csv_filename = os.path.dirname(__file__) + '/validate_ok.csv'
    ocdsextensionregistry.validate.validate_registry_csv()


def test_only_github():
    ocdsextensionregistry.validate.registry_csv_filename = os.path.dirname(__file__) + '/validate_only_github.csv'
    with pytest.raises(Exception) as excinfo:
        ocdsextensionregistry.validate.validate_registry_csv()
    assert 'Repository must be on GitHub' in str(excinfo.value)
