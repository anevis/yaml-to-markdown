from yaml_to_markdown.md_converter import MDConverter

data = {
    "name": "John Doe",
    "age": 30,
    "city": "Sydney",
    "hobbies": ["reading", "swimming"],
}
converter = MDConverter()
with open("output.md", "w") as f:
    converter.convert(data, f)
