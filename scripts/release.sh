#!/usr/bin/env bash
set -euo pipefail
VERSION="${1:?usage: release.sh <version>}"
sed -i "s/^__version__ = .*/__version__ = \"${VERSION}\"/" src/speechloop/__init__.py
git add src/speechloop/__init__.py
git commit -m "chore: bump version to ${VERSION}"
git tag -a "v${VERSION}" -m "release ${VERSION}"
echo "tag v${VERSION} created — git push --tags to publish"
