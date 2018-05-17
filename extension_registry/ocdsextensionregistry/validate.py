import csv
from .models import ExtensionModel


def validate_csv(filename):
    extensions = {}
    with open(filename, 'r') as csvfile:
        reader = csv.reader(csvfile)
        reader.__next__() # Throw away the heading line
        for row in reader:
            extension_id = row[0].lower().strip()
            if extension_id in extensions.keys():
                raise Exception("Extension %s is already registered! (Duplicate is on line %d)" % (extension_id, reader.line_num ))
            extension_model = ExtensionModel(
                repository_url=row[1],
                core=row[2],
                category=row[3]
            )
            extension_model.validate_extension_registry_data_only()
            extensions[extension_id] = extension_model
