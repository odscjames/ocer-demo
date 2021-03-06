import glob, os, json, jinja2, subprocess, shutil, csv, datetime
import extension_website.models

class Builder:
    extension_registry_folder = '/vagrant/extension_registry/extensions/'
    extensions = {}
    website_out_folder = '/out'
    data_folder = '/data'
    standard_versions = ['1.0.3', '1.1.1', '1.1.3']

    def __init__(self):
        pass

    def load_data(self):
        for file in glob.glob(self.extension_registry_folder + '/*.json'):
            if os.path.isfile(file):
                extension_id = file.split('/')[-1].split('.')[0]
                with open(file) as fp:
                    data = json.load(fp)
                    self.extensions[extension_id] = extension_website.models.Extension(
                        github_url=data['github_url'],
                        core=('core' in data and data['core']),
                        category=data['category'],
                        version_as_standard=('version_as_standard' in data and data['version_as_standard']),
                       )

    def fetch_extensions(self):
        for id, data in self.extensions.items():
            # TODO should really make sure data.git_url is a URL to avoid a security problem
            command = "git clone " + data.get_git_clone_url() + '  ' + self.data_folder + '/' + id
            subprocess.check_call(command, shell=True)

    def load_extension_data(self):
        for id in self.extensions.keys():
            # Load the master json
            with open(self.data_folder + '/' + id + '/extension.json') as fp:
                self.extensions[id].extension_data = json.load(fp)
            # Load list of tags
            results = subprocess.check_output("git tag", cwd=self.data_folder + '/' + id, shell=True)
            self.extensions[id].git_tags = results.decode("utf-8") .split('\n')


    def process_data(self):
        for id in self.extensions.keys():
            self.extensions[id].process(standard_versions=self.standard_versions)

    def make_website(self):
        environment = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(os.path.dirname(__file__)) + '/templates/'))
        environment.globals['standard_versions'] = self.standard_versions
        environment.globals['extensions'] = self.extensions
        environment.globals['extension_ids'] = sorted(self.extensions.keys())
        environment.globals['core_extension_ids'] = sorted([id for id, ext in self.extensions.items() if ext.core])
        environment.globals['community_extension_ids'] = sorted([id for id, ext in self.extensions.items() if not ext.core])

        # Index page
        template = environment.get_template('index.html')
        html = template.render()
        self.file_write_data('/en/', 'index.html', html)

        # Table page
        template = environment.get_template('table.html')
        html = template.render()
        self.file_write_data('/en/', 'table.html', html)

        # Table CSV
        with open(self.website_out_folder + '/en/data.csv', 'w') as csvfile:
            writer = csv.writer(csvfile)
            line = [
                'Id',
                'Name',
                'Category',
                'Core'
            ]
            for ver in self.standard_versions:
                line.append('Standard V'+ver)
            writer.writerow(line)
            for id in self.extensions.keys():
                line = [
                    id,
                    self.extensions[id].extension_data['name']['en'],
                    self.extensions[id].category,
                    'yes' if self.extensions[id].core else 'no',
                ]
                for ver in self.standard_versions:
                    line.append('yes' if self.extensions[id].extension_for_standard_versions[ver].available else 'no')
                writer.writerow(line)


        # Index page for each standard
        template = environment.get_template('version/index.html')
        for ver in self.standard_versions:
            html = template.render(
                version=ver,
                version_core_extension_ids=sorted([id for id, ext in self.extensions.items()
                                                   if ext.core and ext.extension_for_standard_versions[ver].available]),
                version_community_extension_ids=sorted([id for id, ext in self.extensions.items()
                                                        if not ext.core and ext.extension_for_standard_versions[ver].available])  #noqa
            )
            self.file_write_data("/en/standard-v" + ver, 'index.html', html)

        # Page for each extension
        template = environment.get_template('extension.html')
        for id, data in self.extensions.items():
            html = template.render(id=id, data=data)
            self.file_write_data('/en/', id + '.html', html)

        # static
        for file in glob.glob(os.path.dirname(os.path.dirname(__file__)) + '/static/*'):
            if os.path.isfile(file):
                shutil.copy(file, self.website_out_folder + '/' + os.path.basename(file))

    def file_write_data(self, path, file_name, html):
        if not os.path.exists(self.website_out_folder + '/' + path):
            os.makedirs(self.website_out_folder + '/' + path)
        with open(self.website_out_folder + '/' + path + '/' + file_name, "w") as f:
            f.write(html)

    def make_legacy_compiled_data(self):
        for ver in self.standard_versions:
            out = {
                "last_updated": str(datetime.datetime.utcnow()),
                "extensions": []
            }

            for extension_id, extension in self.extensions.items():
                if extension.extension_for_standard_versions[ver].available:
                    out_extension = {
                        'slug': extension_id,
                        "category": extension.category,
                        "documentationUrl": {
                            "en": extension.extension_data["documentationUrl"]["en"]
                        },
                        "name": {
                            "en": extension.extension_data["name"]["en"]
                        },
                        "core": extension.core,
                        "url": extension.extension_for_standard_versions[ver].get_url_to_use_in_legacy_compiled_data(),
                        "description": {
                            "en": extension.extension_data["description"]["en"]
                        },
                        "documentation_url": extension.extension_data["documentationUrl"]["en"]
                    }
                    out['extensions'].append(out_extension)

            full_json = json.dumps(out, sort_keys=True, indent=4)
            self.file_write_data('/standard-v' + ver, 'legacy-extensions.json', full_json)
            self.file_write_data('/standard-v' + ver, 'legacy-extensions.js', "extensions_callback(" + full_json + ")")
