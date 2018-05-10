import glob, os, json, jinja2

class Builder:
    extension_registry_folder = '/vagrant/extension_registry/extensions/'
    extensions = {}
    website_out_folder = '/out'

    def __init__(self):
        pass

    def load_data(self):
        for file in glob.glob(self.extension_registry_folder + '/*.json'):
            if os.path.isfile(file):
                extension_id = file.split('/')[-1].split('.')[0]
                with open(file) as fp:
                    self.extensions[extension_id] = json.load(fp)


    def make_website(self):
        template = jinja2.Template(self.file_get_template('extension.html'))
        for id, data in self.extensions.items():
            html = template.render(id=id, data=data)
            self.file_write_html(id+'.html', html)


    def file_get_template(self, template_name):
        with open(os.path.dirname(os.path.dirname(__file__)) + '/templates/' + template_name) as f:
            return f.read()

    def file_write_html(self, file_name, html):
        with open(self.website_out_folder + '/' + file_name, "w") as f:
            f.write(html)