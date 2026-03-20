#!/bin/bash

# Script to extract basic information from a PKT file
# Usage: ./extract-info.sh file.pkt

if [ $# -eq 0 ]; then
    echo "Usage: $0 file.pkt"
    exit 1
fi

PKT_FILE="$1"

if [ ! -f "$PKT_FILE" ]; then
    echo "❌ Error: File not found: $PKT_FILE"
    exit 1
fi

# Temporary name for XML
XML_FILE="/tmp/temp_$(basename "$PKT_FILE" .pkt).xml"

echo "========================================="
echo "  PKT Information Extractor"
echo "========================================="
echo ""
echo "File: $PKT_FILE"
echo ""

# Convert to XML
echo "🔄 Converting to XML..."
if ! ../pka2xml -d "$PKT_FILE" "$XML_FILE" 2>/dev/null; then
    echo "❌ Error converting file"
    exit 1
fi

echo "✅ Conversion completed!"
echo ""

# Extract information
echo "========================================="
echo "  Topology Information"
echo "========================================="
echo ""

# Packet Tracer version
echo "📌 Packet Tracer Version:"
grep -o '<VERSION>[^<]*</VERSION>' "$XML_FILE" | sed 's/<VERSION>//;s/<\/VERSION>//' | head -1
echo ""

# Count devices
echo "📊 Network Devices:"
echo ""

routers=$(grep -c '<TYPE.*>Router</TYPE>' "$XML_FILE" 2>/dev/null || echo 0)
switches=$(grep -c '<TYPE.*>Switch</TYPE>' "$XML_FILE" 2>/dev/null || echo 0)
pcs=$(grep -c '<TYPE.*>Pc</TYPE>' "$XML_FILE" 2>/dev/null || echo 0)
servers=$(grep -c '<TYPE.*>Server</TYPE>' "$XML_FILE" 2>/dev/null || echo 0)

echo "  🔷 Routers: $routers"
echo "  🔶 Switches: $switches"
echo "  💻 PCs: $pcs"
echo "  🖥️  Servers: $servers"

total=$((routers + switches + pcs + servers))
echo ""
echo "  📈 Total devices: $total"
echo ""

# List device names
echo "========================================="
echo "  Device List"
echo "========================================="
echo ""

grep -A 1 '<TYPE.*model=' "$XML_FILE" | grep '<NAME' | sed 's/.*<NAME[^>]*>//;s/<\/NAME>.*//' | nl
echo ""

# Cleanup
rm -f "$XML_FILE"

echo "========================================="
echo "✨ Analysis completed!"
echo "========================================="
echo ""
