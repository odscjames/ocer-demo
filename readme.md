


    python3 /vagrant/extension_registry/compile.py
    python3 /vagrant/extension_registry/validate.py

    PYTHONPATH=$PYTHONPATH:/vagrant/extension_website  python3 /vagrant/extension_website/fetch_and_build.py
    PYTHONPATH=$PYTHONPATH:/vagrant/extension_website  python3 /vagrant/extension_website/build.py
