import extension_website.builder


builder = extension_website.builder.Builder()
builder.load_data()
# We do NOT do builder.fetch_extensions() here
builder.make_website()
