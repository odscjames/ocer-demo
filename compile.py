import os
import json
import sys, glob
import csv

with open('/vagrant/extension_registry/extensions.csv', 'w') as csvfile:
    writer = csv.writer(csvfile)
    line = [
        'Id',
        'GitHubURL',
        'Category',
        'Core'
    ]
    writer.writerow(line)

    for directory in glob.glob("/open-contracting-extension-registry/*"):
        if os.path.isdir(directory):

            id = directory.split('/')[-1]
            print("Input: " + id)

            entry_json_file = os.path.join(directory, "entry.json")

            with open(entry_json_file) as fp:
                entry_obj = json.load(fp)

                url = entry_obj[0]['url']
                if url[-21:] != 'master/extension.json':
                    raise Exception(url[-21:])
                url = url[:-22]

                if url[:33] != 'https://raw.githubusercontent.com':
                    raise Exception(url[:33])
                url = 'https://github.com' + url[33:]

                line = [
                    id,
                    url,
                    entry_obj[0]['category'],
                    entry_obj[0]['core']
                ]

                writer.writerow(line)

