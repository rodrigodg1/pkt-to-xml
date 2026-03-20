#!/bin/bash

# Script to convert multiple PKT files to XML in batch
# Usage: ./batch-convert.sh [directory]

# Define directory (uses current if not specified)
DIRECTORY="${1:-.}"

echo "========================================="
echo "  Batch Converter PKT -> XML"
echo "========================================="
echo ""
echo "Directory: $DIRECTORY"
echo ""

# Counter
total=0
success=0
error=0

# Search for .pkt files
for pkt_file in "$DIRECTORY"/*.pkt; do
    # Check if any file exists
    if [ ! -f "$pkt_file" ]; then
        echo "⚠️  No .pkt files found in $DIRECTORY"
        exit 0
    fi

    # Increment counter
    ((total++))

    # Extract base name (without extension)
    base_name=$(basename "$pkt_file" .pkt)
    xml_file="$DIRECTORY/${base_name}.xml"

    echo "[$total] Converting: $pkt_file"

    # Execute conversion
    if ../pka2xml -d "$pkt_file" "$xml_file" 2>/dev/null; then
        echo "    ✅ Success -> $xml_file"
        ((success++))
    else
        echo "    ❌ Error converting"
        ((error++))
    fi
    echo ""
done

echo "========================================="
echo "  Summary"
echo "========================================="
echo "Total files: $total"
echo "Successfully converted: $success"
echo "Errors: $error"
echo ""
