#!/bin/bash
# use bash strict mode
set -euo pipefail

# Full path to the uploaded repository passed from GitHub Actions
FULL_PATH=$1

if [ -z "$FULL_PATH" ]; then
    echo "Error: Missing full repository path argument." >&2
    exit 1
fi

echo ">>> Stage 1: Updating 'mdwiki' tool core repository..."
echo ">>> FULL_PATH: $FULL_PATH"

# Run deployment steps inside mdwiki's toolforge context
become mdwiki sh -c "cp -rf \"$FULL_PATH/toolforge/deploy_scripts\" /data/project/mdwiki -v;chmod +x /data/project/mdwiki/deploy_scripts/*.sh -v;/data/project/mdwiki/deploy_scripts/update_pybot_local.sh \"$FULL_PATH\""

echo ">>> 'mdwiki' repository update completed successfully."
