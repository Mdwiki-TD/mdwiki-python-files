#!/bin/bash
# Exit immediately if a command exits with a non-zero status
set -e

# Target source path passed from GitHub Actions
SOURCE_PATH=$1

if [ -z "$SOURCE_PATH" ]; then
    echo "Error: Missing source path argument."
    exit 1
fi

# Define all the tool names
tools=("mdwiki")

# Loop through each defined tool
for tool in "${tools[@]}"; do
    # Construct the filename matching the tool name
    filename="${tool}-jobs.yaml"
    FULL_FILE_PATH="${SOURCE_PATH}/$filename"

    echo "Checking for configuration file: $filename"

    # Check if the file actually exists before proceeding
    if [ -f "$FULL_FILE_PATH" ]; then
        # Check if the destination file exists AND is identical to the source file
        if [ -f "/data/project/$tool/$filename" ] && cmp -s "$FULL_FILE_PATH" "/data/project/$tool/$filename"; then
            echo "No changes detected for tool: $tool. Skipping deployment."
            echo "-----------------------------------------------"
            continue
        fi

        echo "Deploying jobs for tool: $tool using file: $filename"

        # Run deployment and ensure internal commands exit with error if they fail
        become "$tool" sh -c "cp \"$FULL_FILE_PATH\" \$HOME/$filename; tfj flush; tfj load $filename"

        echo "Successfully deployed jobs for tool: $tool"
        echo "-----------------------------------------------"
    fi
done
