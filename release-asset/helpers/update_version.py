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


def inplace_change(filename, old_string, new_string):
    # Safely read the input filename using 'with'
    with open(filename) as f:
        s = f.read()
        if old_string not in s:
            print('"{old_string}" not found in {filename}.'.format(**locals()))
            return

    # Safely write the changed content, if found in the file
    with open(filename, "w") as f:
        print(
            'Changing "{old_string}" to "{new_string}" in {filename}'.format(**locals())
        )
        s = s.replace(old_string, new_string)
        f.write(s)


with open(manifest_file, "r") as manifest:
    manifest_data = json.load(manifest)
    old_version = manifest_data["version"]

inplace_change(manifest_file, old_version, version)
