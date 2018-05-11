import jsonschema, os, glob, json


def validate():
    with open(os.path.dirname(__file__) + '/entry-schema.json') as fp:
        schema = json.load(fp)
    for file_name in glob.glob(os.path.dirname(__file__) + '/extensions/*.json'):
        if os.path.isfile(file_name):
            print(file_name)
            with open(file_name) as fp:
                jsonschema.validate(json.load(fp), schema)

if __name__ == "__main__":
    validate()
