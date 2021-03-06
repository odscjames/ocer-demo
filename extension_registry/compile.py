import ocdsextensionregistry.compile
import os


if __name__ == "__main__":
    ocdsextensionregistry.compile.registry_csv_filename = \
        os.path.join(os.path.dirname(__file__), 'extensions.csv')

    ocdsextensionregistry.compile.extensions_repositories_folder = \
        os.path.join(os.path.dirname(__file__), "extensions_repositories")
    if not os.path.isdir(ocdsextensionregistry.compile.extensions_repositories_folder):
        os.makedirs(ocdsextensionregistry.compile.extensions_repositories_folder)

    ocdsextensionregistry.compile.output_folder = \
        os.path.join(os.path.dirname(__file__), "output")
    if not os.path.isdir(ocdsextensionregistry.compile.output_folder):
        os.makedirs(ocdsextensionregistry.compile.output_folder)

    ocdsextensionregistry.compile.legacy_output_folder = \
        os.path.join(os.path.dirname(__file__), "legacy_output")
    if not os.path.isdir(ocdsextensionregistry.compile.legacy_output_folder):
        os.makedirs(ocdsextensionregistry.compile.legacy_output_folder)

    ocdsextensionregistry.compile.compile_registry()
