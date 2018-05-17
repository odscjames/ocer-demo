import csv
from .models import ExtensionModel
from .util import string_to_boolean
import os
import subprocess
import json

registry_csv_filename = None
extensions_repositories_folder = None
standard_versions = ['1.0.3', '1.1.1', '1.1.3']
output_folder = None

_extensions = {}


def compile_registry():
    if registry_csv_filename is None:
        raise Exception("Please set registry_csv_filename")
    if extensions_repositories_folder is None:
        raise Exception("Please set extensions_repositories_folder")
    if output_folder is None:
        raise Exception("Please set output_folder")
    _load_data()
    _fetch_extensions()
    _load_extension_data()
    _process_data()
    _make_output()


def _load_data():
    with open(registry_csv_filename, 'r') as csvfile:
        reader = csv.reader(csvfile)
        reader.__next__()  # Throw away the heading line
        for row in reader:
            # To decide if row has any data in, check it has values and it has an id.
            if len(row) > 0:
                extension_id = row[0].lower().strip()
                if extension_id:
                    if extension_id in _extensions.keys():
                        raise Exception("Extension %s is already registered! (Duplicate is on line %d)" % (
                            extension_id, reader.line_num))
                    extension_model = ExtensionModel(
                        repository_url=row[1],
                        category=row[2],
                        core=string_to_boolean(row[3])
                    )
                    _extensions[extension_id] = extension_model


def _fetch_extensions():
    for extension_id, data in _extensions.items():
        folder = os.path.join(extensions_repositories_folder,  extension_id)
        if os.path.isdir(folder):
            pass
            # TODO git fetch
        else:
            # TODO should really make sure data.git_url is a URL to avoid a security problem
            command = "git clone " + data.get_git_clone_url() + '  ' + folder
            subprocess.check_call(command, shell=True)


def _load_extension_data():
    for extension_id in _extensions.keys():
        # Load the master json
        with open(os.path.join(extensions_repositories_folder,  extension_id, 'extension.json')) as fp:
            _extensions[extension_id].extension_data = json.load(fp)
        # Load list of tags
        results = subprocess.check_output(
            "git tag",
            cwd=os.path.join(extensions_repositories_folder, extension_id),
            shell=True
        )
        _extensions[extension_id].git_tags = results.decode("utf-8") .split('\n')


def _process_data():
    for extension_id in _extensions.keys():
        _extensions[extension_id].process(standard_versions=standard_versions)


def _make_output():
    with open(os.path.join(output_folder, 'full_data.csv'), 'w') as csvfile:
        writer = csv.writer(csvfile)
        line = [
            'Id',
            'Name',
            'Category',
            'Core'
        ]
        for ver in standard_versions:
            line.append('Standard V' + ver)
        writer.writerow(line)
        for id in _extensions.keys():
            line = [
                id,
                _extensions[id].extension_data['name']['en'],
                _extensions[id].category,
                'yes' if _extensions[id].core else 'no',
            ]
            for ver in standard_versions:
                line.append('yes' if _extensions[id].extension_for_standard_versions[ver].available else 'no')
            writer.writerow(line)
