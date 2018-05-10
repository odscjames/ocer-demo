import extension_website.builder


builder = extension_website.builder.Builder()
builder.load_data()
builder.fetch_extensions()
builder.make_website()
