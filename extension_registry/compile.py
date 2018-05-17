import ocdsextensionregistry.compile
import os


if __name__ == "__main__":
    ocdsextensionregistry.compile.registry_csv_filename = \
        os.path.join(os.path.dirname(__file__), 'extensions.csv')
    ocdsextensionregistry.compile.extensions_repositories_folder = \
        os.path.join(os.path.dirname(__file__), "extensions_repositories")
    ocdsextensionregistry.compile.compile_registry()
