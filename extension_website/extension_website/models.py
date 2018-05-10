

class Extension:

    def __init__(self, github_url, core, version_as_standard, category):
        self.github_url = github_url
        self.core = core
        self.version_as_standard = version_as_standard
        self.extension_for_standard_versions = {}
        self.extension_data = None
        self.git_tags = []
        self.category = category

    def process(self, standard_versions):
        for ver in standard_versions:
            self.extension_for_standard_versions[ver] = ExtensionForStandardVersion(extension=self)
            if self.version_as_standard:
                if 'v' + ver in self.git_tags:
                    self.extension_for_standard_versions[ver].git_reference = 'v' + ver
                else:
                    self.extension_for_standard_versions[ver].available = False

    def get_git_clone_url(self):
        if self.github_url[-1:] == '/':
            return self.github_url[:-1] + '.git'
        else:
            return self.github_url + '.git'


class ExtensionForStandardVersion:

    def __init__(self, extension):
        self.extension = extension
        self.available = True
        self.git_reference = 'master'

    def get_url_to_use_in_standard_extensions_list(self):
        url_bits = self.extension.github_url.split('/')
        url = 'https://raw.githubusercontent.com/' + url_bits[3] + '/' + url_bits[4] + '/' + \
              self.git_reference + '/extension.json'
        return url
