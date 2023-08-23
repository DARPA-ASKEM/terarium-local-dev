#! venv/bin/python
import argparse
import json
import os

from build.components import extract_components
from build.compose import AskemComposer, AskemComposerException

cwd = os.path.dirname(os.path.realpath(__file__))
component_dir = f"{cwd}/components"


if __name__ == "__main__":
    # Initialize parser
    parser = argparse.ArgumentParser()
    parser.add_argument("-e", "--env", help="Custom env file to write out.", default="test.env")
    parser.add_argument(
        "-l", "--local", help="Flag that sets up the build as full local install."
    )
    parser.add_argument(
        "-s", "--staging", help="Flag that sets up the job as a staging install."
    )
    parser.add_argument(
        "-x",
        "--extract",
        help="Flag that sets up the job as an extraction to write "
             "new services to the components directory."
    )

    args = parser.parse_args()
    yaml_file = f"{cwd}/docker-compose.yml"
    if args.extract:
        extract_components(file_path=yaml_file, component_dir=component_dir)
    else:
        with open(f"{cwd}/services.json") as config:
            composer = AskemComposer(
                local=args.local == 'true',
                staging=args.staging == 'true' and args.local != 'true',
                config=json.loads(config.read()),
                compose_file=yaml_file,
                env_file=f"{cwd}/{args.env}",
                working_dir=cwd,
            )
        try:
            os.system("clear")
            composer.setup()
            composer.write_env()
            composer.write_compose_file()
        except AskemComposerException as e:
            print(e.message)
            exit(1)
