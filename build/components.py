from pathlib import Path
from ruamel.yaml import YAML
from build import get_base_yaml


def extract_components(file_path: str, component_dir: str):
    yaml = YAML()
    yaml_file = yaml.load(Path(file_path))

    for service in yaml_file["services"]:
        save_service_file(
            name=service,
            component_dir=component_dir,
            service_definition=yaml_file["services"][service],
        )


def save_service_file(name: str, component_dir: str, service_definition: dict):
    print(f"Saving {name} service.")
    component_file = f"{component_dir}/{name}.yml"
    with open(component_file, "w") as cfile:
        yaml = get_base_yaml()
        dump_obj = {f"{name}": service_definition}
        yaml.dump(dump_obj, cfile)
