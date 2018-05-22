import os
import json
import sys, glob
import csv

for directory in glob.glob("/open-contracting-extension-registry/*"):
    if os.path.isdir(directory):

        id = directory.split('/')[-1]
        print("Id: " + id)
        print("")

        registry_json_file = os.path.join(directory, "entry.json")

        with open(registry_json_file) as fp:
            registry_obj = json.load(fp)

        extension_json_file = os.path.join("/vagrant/real_extension_registry/extensions_repositories/" + id.lower() + "/extension.json")

        with open(extension_json_file) as fp:
            extension_obj = json.load(fp)


        if registry_obj[0]['name']['en'] != extension_obj['name']['en']:
            print("Name Different!")
            print("Registry: " + registry_obj[0]['name']['en'])
            print("Extension: " + extension_obj['name']['en'])
            print("")

        if registry_obj[0]['description']['en'] != extension_obj['description']['en']:
            print("Description Different!")
            print("Registry: " + registry_obj[0]['description']['en'])
            print("Extension: " + extension_obj['description']['en'])
            print("")

        if registry_obj[0]['documentationUrl']['en'] != extension_obj['documentationUrl']['en']:
            print("documentationUrl Different!")
            print("Registry: " + registry_obj[0]['documentationUrl']['en'])
            print("Extension: " + extension_obj['documentationUrl']['en'])
            print("")

        url_bits = registry_obj[0]['url'].split('/')
        url = 'https://github.com/' + url_bits[3] + '/' + url_bits[4] + '/blob/master/extension.json'

        print("Please make "+ url + " have the correct value")
        print("")

