

class Extension:
    github_url = None
    core = None
    extension_data = None
    standard_versions = {}

    def __init__(self, github_url, core):
        self.github_url = github_url
        self.core = core

    def process(self, standard_versions):
        for ver in standard_versions:
            self.standard_versions[ver] = ExtensionForStandardVersion

    def get_git_clone_url(self):
        if self.github_url[-1:] == '/':
            return self.github_url[:-1] + '.git'
        else:
            return self.github_url + '.git'


class ExtensionForStandardVersion:
    available = True

    def __init__(self):
        pass
