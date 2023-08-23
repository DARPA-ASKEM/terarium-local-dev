import os
from pathlib import Path
from ruamel.yaml import YAML
from build import get_base_yaml
import sys


class AskemComposerException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__()


class AskemComposer:
    _component_path = "{working_dir}/components/{service}.yml"
    _compose_yaml = {
        "version": "3",
        "services": {},
        "volumes": {
            "minio-data": {"driver": "local"},
            "terarium-db-storage": {"driver": "local"},
        },
    }

    def __init__(self, **kwargs):
        self.build_manifest = []
        self.env_vars = {}
        for k in kwargs:
            self.__setattr__(k, kwargs[k])

    def setup(self):
        for key in self.config:
            os.system("clear")
            enable_service = input(f"Enable local service {key}? (y/N)")
            if enable_service.lower() in ["y", "yes"]:
                service_key = self.config[key]["key"]
                image_key = f"{service_key}_IMG"
                version_key = f"{service_key}_VERSION"
                version = self.config[key]["build_env"][version_key]
                buildable = self.config[key]["buildable"]
                local_build = input("Local build? (y/N)") if buildable else False
                if local_build.lower() in ["y", "yes"]:
                    build_path = input("Path to repository?")
                    if "~" in build_path:
                        build_path = build_path.replace("~", os.environ["HOME"])
                    if os.path.exists(Path(build_path)) is False:
                        raise AskemComposerException(
                            f"Path {build_path} does not exist"
                        )
                    build_key = self.config[key]["build_path"]
                    image_to_use = f"{key}-local"
                    self.env_vars[build_key] = build_path
                    version = "latest"
                    self.build_manifest.append(key)
                else:
                    default_image = self.config[key]["env"][image_key]
                    use_default = input(f"Use default image [{default_image}]? (y/N)")
                    if use_default.lower() in ["y", "yes"]:
                        image_to_use = default_image
                    else:
                        image_to_use = input(f"Image to use for {key}?")
                        image_version = input(f"Image version? Defaults to latest")
                        if image_version:
                            version = image_version
                self.env_vars[version_key] = version
                self.env_vars[image_key] = image_to_use
                self._process_service_env(service=key)

    def write_env(self) -> None:
        """
        Method writes out the build env file.
        """
        with open(self.env_file, "w") as env_file:
            for k in self.env_vars:
                value = self.env_vars[k]
                env_file.write(f"{k}={value}\n")

    def write_compose_file(self) -> None:
        compose_yaml = get_base_yaml()

        for service in self.config:
            if service in self._compose_yaml["services"]:
                continue
            service_compose_file = self._component_path.format(
                working_dir=self.working_dir, service=service
            )
            yaml_file = self._load_yaml(service_compose_file)
            if service not in self.build_manifest and "build" in yaml_file[service]:
                del yaml_file[service]["build"]
            self._compose_yaml["services"][service] = yaml_file[service]
            if "depends_on" in yaml_file[service]:
                self._handle_dependencies(yaml_file[service]["depends_on"])
        with open(self.compose_file, "w") as cfile:
            compose_yaml.dump(self._compose_yaml, cfile)

    def teardown(self):
        pass

    @staticmethod
    def _load_yaml(yaml_path: str) -> YAML:
        """
        Static method loads a yaml object.
        :param yaml_path:
        """
        yaml_file = YAML()
        return yaml_file.load(Path(yaml_path))

    def _handle_dependencies(self, dependencies: dict) -> None:
        """
        Method processes a service's dependencies.
        :param dependencies:
        :return:
        """
        for d in dependencies:
            if d in self._compose_yaml["services"]:
                continue
            dep_yaml = self._component_path.format(
                working_dir=self.working_dir, service=d
            )
            dep_yaml_obj = self._load_yaml(dep_yaml)
            self._compose_yaml["services"][d] = dep_yaml_obj[d]
            if "depends_on" in dep_yaml_obj[d]:
                self._handle_dependencies(dep_yaml_obj[d]["depends_on"])

    def _process_service_env(self, service: str) -> None:
        """
        Method processes the service env
        :param service: The service to process
        """
        service_items = self.config[service]["env"]
        os.system("clear")
        for item in service_items:
            if item in self.env_vars:
                continue
            default_value = service_items[item]
            item_value = input(f"Use default ({default_value}) for {item}? (Y/n)")
            if item_value.lower() in ["n", "no"]:
                custom_value = input(f"Enter custom value for {item}:")
                item_value = custom_value
            else:
                item_value = default_value
            self.env_vars[item] = item_value
