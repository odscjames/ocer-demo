import glob, os, json, jinja2, subprocess

class Builder:
    extension_registry_folder = '/vagrant/extension_registry/extensions/'
    extensions = {}
    website_out_folder = '/out'
    data_folder = '/data'
    standard_versions = ['1.0.3', '1.1.3']

    def __init__(self):
        pass

    def load_data(self):
        for file in glob.glob(self.extension_registry_folder + '/*.json'):
            if os.path.isfile(file):
                extension_id = file.split('/')[-1].split('.')[0]
                with open(file) as fp:
                    self.extensions[extension_id] = json.load(fp)

    def fetch_extensions(self):
        for id, data in self.extensions.items():
            command = "git clone " + data['url'] + '  ' + self.data_folder + '/' + id
            subprocess.check_call(command, shell=True)

    def load_extension_data(self):
        for id in self.extensions.keys():
            with open(self.data_folder + '/' + id + '/extension.json') as fp:
                self.extensions[id]['extension_data'] = json.load(fp)

    def make_website(self):
        environment = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(os.path.dirname(__file__)) + '/templates/'))

        # Index page
        template = environment.get_template('index.html')
        html = template.render(ids=self.extensions.keys(), data=self.extensions, standard_versions=self.standard_versions)
        self.file_write_html('/', 'index.html', html)

        # Index page for each standard
        template = environment.get_template('version/index.html')
        for ver in self.standard_versions:
            html = template.render(version=ver)
            self.file_write_html("standard-v"+ver, 'index.html', html)



        # Page for each extension
        template = environment.get_template('extension.html')
        for id, data in self.extensions.items():
            html = template.render(id=id, data=data)
            self.file_write_html('/', id+'.html', html)

    def file_write_html(self, path, file_name, html):
        if not os.path.exists(self.website_out_folder + '/' + path):
            os.makedirs(self.website_out_folder + '/' + path)
        with open(self.website_out_folder + '/' + path + '/' + file_name, "w") as f:
            f.write(html)
