"""Update manifest for current release version."""
import json
import os
import sys

print(sys.argv)
COMPONENT = sys.argv[4]

version = str(sys.argv[2])
version = version[version.find("tags/")+5:]

print(f"Version to update to {version}")

manifest_file = f"{os.getcwd()}/custom_components/{COMPONENT}/manifest.json"
# manifest_file = f"{os.getcwd()}/../manifest.json"


with open(manifest_file, "r") as manifest:
    manifest_data = json.load(manifest)
    manifest_data["version"] = version

with open(manifest_file, "w") as manifest:
    json.dump(manifest_data, manifest, indent=2)