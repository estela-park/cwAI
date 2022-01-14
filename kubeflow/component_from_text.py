import kfp

hello_op = kfp.components.load_component_from_text('''
implementation:
  container:
    image: alpine
    command: ["echo", "Hello world"]
''')

print(type(hello_op))