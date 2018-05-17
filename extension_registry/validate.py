import ocdsextensionregistry.validate
import os

if __name__ == "__main__":
    ocdsextensionregistry.validate.validate_csv(os.path.dirname(__file__) + '/extensions.csv')
