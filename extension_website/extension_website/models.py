

class Extension:
    git_url = None
    core = None
    extension_data = None
    standard_versions = {}

    def __init__(self, git_url, core):
        self.git_url = git_url
        self.core = core

    def process(self, standard_versions):
        for ver in standard_versions:
            self.standard_versions[ver] = ExtensionForStandardVersion


class ExtensionForStandardVersion:
    available = True

    def __init__(self):
        pass
