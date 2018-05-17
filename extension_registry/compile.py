import ocdsextensionregistry.compile
import os


if __name__ == "__main__":
    ocdsextensionregistry.compile.registry_csv_filename = os.path.dirname(__file__) + '/extensions.csv'
    ocdsextensionregistry.compile.compile_registry()
