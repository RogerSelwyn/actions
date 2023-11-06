# actions 

## Release Asset

_Updates the version number in the manifest in line with the release, and creates a release asset._

### Inputs

| Input          | Description                                                                        |
| -------------- | ---------------------------------------------------------------------------------- |
| github_token   | Github token to enable change commits.                                             |
| component      | Name of the HA integration component being released.                               |

### Example

```yaml
name: Component Release

on:
  release:
    types: [published]

jobs:
  release_zip_file:
    name: Prepare release asset
    runs-on: "ubuntu-latest"
    steps:
      - uses: "actions/checkout@v2"
      - name: Release Asset
        uses: "rogerselwyn/actions/release-asset@main"
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          component: O365
```

## Release Notes

_Creates a draft version of the release notes based on commites._

### Inputs

| Input          | Description                                                                        |
| -------------- | ---------------------------------------------------------------------------------- |
| github_token   | Github token to enable change commits.                                             |

### Example

```yaml
name: Component Release

on:
  release:
    types: [published]

jobs:
  releasenotes:
    name: Prepare release notes
    runs-on: "ubuntu-latest"
    steps:
      - uses: "actions/checkout@v2"
      - name: Release Asset
        uses: "rogerselwyn/actions/release-notes@main"
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
```
