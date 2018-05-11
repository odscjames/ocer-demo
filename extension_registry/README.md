# Extension Repository

The place where extensions can be registered in order to appear in the docs.

Each extension lives in its own json file in this repo, in the _extensions_ folder. The file must follow the format described in the schema file _entry-schema.json_.

Each json file must validate against the schema before being included in the registry.

## extension-id.json

### Required fields

* `category`: part of the docs the extensions appears in.
* `github_url`: URL of the extension repository. eg https://github.com/open-contracting/ocds_bid_extension

### Optional fields

* `core`: a boolean declaring the extension core (true) or community (false).
* `version_as_standard`: a boolean declaring whether the extension has versions that are locked to the versions of the standard (normally only core extensions have this).

Here is an example :

```json
{
    "category": "bids",
    "core": true,
    "github_url": "https://github.com/open-contracting/ocds_bid_extension",
    "version_as_standard": true
}
```

## Maintenance

Install dependencies:

    pip install -r requirements.txt

Validate entries:

    python validate.py

To build an site with more information, see XXXXXXXXXX
