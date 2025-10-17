#!/bin/bash

# WordPress Batch Sync for Publisher Edition (skylerthomas3)
# Syncs files from sync-list2.sh using wp-sync-rest.js from SkylerThomas directory

# Use wp-sync-rest.js from the SkylerThomas directory (shared dependency)
SCRIPT_PATH="/Users/paulmarshall/Documents/GitHub/SkylerThomas/wp-sync-rest.js"

# Source the file list (specific to this sync)
source ./sync-list2.sh

echo "========================================="
echo "WordPress Batch Sync - Publisher Edition"
echo "========================================="
echo ""
echo "Source: skylerthomas3.wiki (REVISED chapters)"
echo "Using: wp-sync-rest.js from SkylerThomas"
echo ""

# Count files
file_count=${#FILES[@]}

echo "Found $file_count files in sync list"
echo ""

# Counter
current=0
success=0
failed=0

# Loop through each file in the list
for filepath in "${FILES[@]}"; do
    current=$((current + 1))
    filename=$(basename "$filepath")

    echo "[$current/$file_count] Syncing: $filename"
    echo "----------------------------------------"

    # Check if file exists
    if [ ! -f "$filepath" ]; then
        echo "✗ File not found: $filepath"
        failed=$((failed + 1))
        echo ""
        continue
    fi

    # Run the sync script
    $SCRIPT_PATH "$filepath"

    # Check exit status
    if [ $? -eq 0 ]; then
        echo "✓ Success!"
        success=$((success + 1))
    else
        echo "✗ Failed to sync $filename"
        failed=$((failed + 1))
    fi

    echo ""
done

echo "========================================="
echo "Batch sync complete!"
echo "Processed: $file_count files"
echo "Success: $success"
echo "Failed: $failed"
echo "========================================="
