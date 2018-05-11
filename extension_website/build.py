import extension_website.builder


builder = extension_website.builder.Builder()
builder.load_data()
# We do NOT do builder.fetch_extensions() here
builder.load_extension_data()
builder.process_data()
builder.make_website()
builder.make_legacy_compiled_data()
