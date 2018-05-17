

class ExtensionModel:

    def __init__(self, repository_url, core, category):
        self.repository_url = repository_url
        self.core = core
        self.category = category

    def validate_extension_registry_data_only(self):
        if self.repository_url[:19] != 'https://github.com/':
            raise Exception("Repository must be on GitHub")
