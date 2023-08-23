from ruamel.yaml import YAML


def get_base_yaml():
    yaml = YAML()
    yaml.indent(mapping=2, sequence=4, offset=2)
    return yaml
