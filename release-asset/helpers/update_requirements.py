import json
import os
import sys

COMPONENT = sys.argv[2]


with open(
    f"{os.getcwd()}/custom_components/{COMPONENT}/manifest.json", "r"
) as manifest:
    manifest = json.load(manifest)
    requirements = []
    for req in manifest["requirements"]:
        requirements.append(req)


print(json.dumps(manifest["requirements"], indent=4, sort_keys=True))

with open(f"{os.getcwd()}/requirements.txt", "w") as requirementsfile:
    for req in requirements:
        requirementsfile.write(req + "\n")
