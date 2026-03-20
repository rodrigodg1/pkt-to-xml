# Usage Examples

This folder contains example scripts to facilitate the use of the PKT/XML conversion tool.

## Available Scripts

### 1. batch-convert.sh

Converts multiple `.pkt` files to `.xml` in batch.

**Usage:**
```bash
# Convert all .pkt files in the current directory
./batch-convert.sh

# Convert all .pkt files in a specific directory
./batch-convert.sh /path/to/directory
```

**Example output:**
```
=========================================
  Batch Converter PKT -> XML
=========================================

Directory: ./networks

[1] Converting: ./networks/network1.pkt
    ✅ Success -> ./networks/network1.xml

[2] Converting: ./networks/network2.pkt
    ✅ Success -> ./networks/network2.xml

=========================================
  Summary
=========================================
Total files: 2
Successfully converted: 2
Errors: 0
```

### 2. extract-info.sh

Extracts and displays network topology information without opening Packet Tracer.

**Usage:**
```bash
./extract-info.sh file.pkt
```

**Example output:**
```
=========================================
  PKT Information Extractor
=========================================

File: my_network.pkt

🔄 Converting to XML...
✅ Conversion completed!

=========================================
  Topology Information
=========================================

📌 Packet Tracer Version:
9.0.0.0810

📊 Network Devices:

  🔷 Routers: 2
  🔶 Switches: 3
  💻 PCs: 5
  🖥️  Servers: 1

  📈 Total devices: 11

=========================================
  Device List
=========================================

     1	Router0
     2	Router1
     3	Switch0
     4	Switch1
     5	Switch2
     6	PC0
     7	PC1
     8	PC2
     9	PC3
    10	PC4
    11	Server0

=========================================
✨ Analysis completed!
=========================================
```

## How to Use the Scripts

1. **Make the scripts executable:**
```bash
chmod +x batch-convert.sh
chmod +x extract-info.sh
```

2. **Run as needed:**
```bash
./extract-info.sh my_file.pkt
```

## Tips

- Scripts assume the `pka2xml` executable is in the parent directory (`../pka2xml`)
- You can modify the scripts for your specific needs
- Use the scripts as a base to create your own automations

## Student Activities

### Activity 1: Comparative Analysis
Compare two network topologies by converting them to XML and using `diff`:
```bash
./pka2xml -d network1.pkt network1.xml
./pka2xml -d network2.pkt network2.xml
diff network1.xml network2.xml
```

### Activity 2: Device Counting
Use Linux commands to count how many devices of each type exist:
```bash
grep -o '<TYPE.*>Router</TYPE>' topology.xml | wc -l
```

### Activity 3: Configuration Extraction
Extract all IP configurations from the network:
```bash
grep -i 'ipv4address' topology.xml
```

### Activity 4: Bulk Modification
Create a script that:
1. Converts a `.pkt` to XML
2. Modifies all IP addresses from one subnet to another
3. Converts back to `.pkt`

Example with `sed`:
```bash
./pka2xml -d original.pkt temp.xml
sed 's/192\.168\.1\./192.168.2./g' temp.xml > modified.xml
./pka2xml -e modified.xml new.pkt
```

## Advanced Examples

### Example 1: Extract Only Router Configurations
```bash
#!/bin/bash
./pka2xml -d network.pkt network.xml
grep -A 50 '<TYPE.*>Router</TYPE>' network.xml > routers_only.txt
```

### Example 2: Generate Network Report
```bash
#!/bin/bash
PKT_FILE="$1"
./pka2xml -d "$PKT_FILE" temp.xml

echo "Network Report"
echo "=============="
echo "File: $PKT_FILE"
echo ""
echo "Devices:"
echo "- Routers: $(grep -c '<TYPE.*>Router</TYPE>' temp.xml)"
echo "- Switches: $(grep -c '<TYPE.*>Switch</TYPE>' temp.xml)"
echo "- PCs: $(grep -c '<TYPE.*>Pc</TYPE>' temp.xml)"

rm temp.xml
```

### Example 3: Validate Topology
```bash
#!/bin/bash
# Check if topology meets requirements

./pka2xml -d student_work.pkt work.xml

routers=$(grep -c "Router" work.xml)
switches=$(grep -c "Switch" work.xml)
pcs=$(grep -c "Pc" work.xml)

score=0

[ $routers -ge 2 ] && ((score+=33)) && echo "✅ Has 2+ routers"
[ $switches -ge 1 ] && ((score+=33)) && echo "✅ Has 1+ switches"
[ $pcs -ge 3 ] && ((score+=34)) && echo "✅ Has 3+ PCs"

echo ""
echo "Score: $score/100"

rm work.xml
```

## For Educators

### Create Exercise Templates

```bash
#!/bin/bash
# Generate 10 variations of an exercise

./pka2xml -d base_template.pkt template.xml

for i in {1..10}; do
    # Replace placeholders
    sed -e "s/STUDENT_NAME/Student_$i/g" \
        -e "s/192.168.1/192.168.$i/g" \
        template.xml > student_$i.xml

    # Convert back to PKT
    ./pka2xml -e student_$i.xml exercise_$i.pkt

    echo "Generated: exercise_$i.pkt"
done
```

### Automated Grading

```bash
#!/bin/bash
# Simple grading script

for file in submissions/*.pkt; do
    student=$(basename "$file" .pkt)
    ./pka2xml -d "$file" temp.xml

    # Check requirements
    has_router=$(grep -c "Router" temp.xml)
    has_switch=$(grep -c "Switch" temp.xml)

    if [ $has_router -ge 1 ] && [ $has_switch -ge 1 ]; then
        echo "$student: PASS"
    else
        echo "$student: FAIL (missing devices)"
    fi

    rm temp.xml
done
```

## Need More Examples?

- Check the main [README.md](../README.md)
- See [FAQ.md](../FAQ.md) for common questions
- Open an issue on GitHub to request specific examples

---

**Happy automating!** 🚀
