import os
import json
import sys, glob


for directory in glob.glob("/open-contracting-extension-registry/*"):
    if os.path.isdir(directory):

        id = directory.split('/')[-1]
        print(id)

        entry_json_file = os.path.join(directory, "entry.json")
        out_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), "extensions", id + ".json")

        with open(entry_json_file) as fp:
            entry_obj = json.load(fp)

            url = entry_obj[0]['url']
            if url[-21:] != 'master/extension.json':
                raise Exception(url[-21:])
            url = url[:-22] + '.git'

            if url[:33] != 'https://raw.githubusercontent.com':
                raise Exception(url[:33])
            url = 'https://github.com' + url[33:]

            out_data = {
                "core":entry_obj[0]['core'],
                "url":url,
            }

            with open(out_file, 'w') as outfile:
                json.dump(out_data, outfile, indent=4)


