# ❓ Frequently Asked Questions (FAQ)

## General

### What is this tool?

A converter that transforms Cisco Packet Tracer files (`.pkt` and `.pka`) into readable XML and vice versa. Useful for analyzing, modifying, and automating network topology creation.

### Why convert PKT to XML?

- 📖 **Visualize** network structure in text format
- ✏️ **Edit** configurations without opening Packet Tracer
- 🔍 **Analyze** topologies programmatically
- 🤖 **Automate** exercise creation
- 📊 **Compare** different topology versions
- 🔄 **Version control** with Git (XML is diff-friendly)

### What's the difference between .pkt and .pka?

- **`.pkt`** = Packet Tracer file (simple network topology)
- **`.pka`** = Packet Tracer Activity (includes instructions, scoring, etc.)

The tool works with both!

## Compatibility

### Which Packet Tracer versions are supported?

✅ **Supported:**
- Packet Tracer 7.x
- Packet Tracer 8.x
- Packet Tracer 9.x

❌ **NOT directly supported:**
- Packet Tracer 5.x (use original `ptexplorer`)
- Packet Tracer 6.x (may work, not tested)

### Does it work on Windows?

Currently, the tool is tested on:
- ✅ macOS (Intel and Apple Silicon)
- ✅ Linux (Ubuntu, Debian, Fedora)
- ⚠️ Windows with WSL (Windows Subsystem for Linux)
- ❌ Native Windows (requires manual compilation)

**For Windows**: We recommend using WSL2.

### Does it work on Raspberry Pi?

Yes! If you have the dependencies installed:
```bash
sudo apt-get install build-essential libcryptopp-dev libre2-dev zlib1g-dev
```

## Installation

### "brew: command not found"

You're on macOS and don't have Homebrew installed. Install with:
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### Error: "libcryptopp.so: cannot open shared object file"

Libraries are not installed. Run:

**Ubuntu/Debian:**
```bash
sudo apt-get install libcryptopp-dev libre2-dev zlib1g-dev
```

**macOS:**
```bash
brew install cryptopp re2
```

### Compilation error: "C++17 required"

Your compiler is too old. Update:

**Ubuntu:**
```bash
sudo apt-get install g++-9
```

**macOS:**
```bash
xcode-select --install
```

## Usage

### How to convert PKT to XML?

```bash
./pka2xml -d file.pkt output.xml
```

### How to convert XML back to PKT?

```bash
./pka2xml -e file.xml output.pkt
```

### Can I open the converted PKT in Packet Tracer?

Yes! If you:
1. Converted PKT → XML
2. Edited the XML
3. Converted XML → PKT

The generated `.pkt` file can be opened in Packet Tracer normally.

**⚠️ Warning**: Invalid edits in XML may result in corrupted file!

### The XML file is very large, is this normal?

Yes! A 50KB `.pkt` file can generate a 700KB+ XML because:
- XML is uncompressed text
- Contains ALL detailed configurations
- Includes binary data in Base64

### Can I edit the XML manually?

Yes, but carefully:

✅ **Safe to edit:**
- Device names (`<NAME>`)
- IP addresses
- Descriptions
- IOS configurations

❌ **DO NOT edit:**
- XML structure (tags)
- Base64 data
- Internal IDs
- Checksums

**Tip**: Always backup before editing!

### How to view only basic info without converting everything?

Use the example script:
```bash
cd examples
./extract-info.sh ../file.pkt
```

## Modification and Editing

### Can I change all IPs in a network?

Yes! Use `sed`:
```bash
# Convert to XML
./pka2xml -d network.pkt network.xml

# Change 192.168.1.x to 192.168.2.x
sed -i 's/192\.168\.1\./192.168.2./g' network.xml

# Convert back
./pka2xml -e network.xml new_network.pkt
```

### Can I add devices by editing XML?

Technically yes, but it's **very complex**. We recommend:
1. Add in Packet Tracer
2. Then convert for analysis/modification

### How to compare two topologies?

```bash
./pka2xml -d network1.pkt network1.xml
./pka2xml -d network2.pkt network2.xml
diff network1.xml network2.xml
```

Or use visual tools like `meld`:
```bash
meld network1.xml network2.xml
```

## For Educators

### How to automatically create varied exercises?

1. Create a template in Packet Tracer
2. Convert to XML
3. Use scripts to generate variations:

```bash
./pka2xml -d template.pkt template.xml

for i in {1..30}; do
    sed "s/CLASS_X/CLASS_$i/g" template.xml > class_$i.xml
    ./pka2xml -e class_$i.xml exercise_class_$i.pkt
done
```

### How to verify if students completed the exercise correctly?

```bash
# Convert student work
./pka2xml -d student_work.pkt work.xml

# Check requirements
routers=$(grep -c "Router" work.xml)

if [ $routers -ge 2 ]; then
    echo "Passed: Has $routers routers"
else
    echo "Failed: Missing routers"
fi
```

### How to extract IOS configurations?

```bash
./pka2xml -d network.pkt network.xml
grep -A 100 "<CONFIG>" network.xml
```

## Common Problems

### "error opening input file"

**Causes:**
1. File doesn't exist
2. Wrong path
3. No read permission

**Solution:**
```bash
# Check if exists
ls -la file.pkt

# Use absolute path
./pka2xml -d /full/path/file.pkt output.xml

# Give permission
chmod 644 file.pkt
```

### "Permission denied: ./pka2xml"

Make it executable:
```bash
chmod +x pka2xml
```

### The generated PKT file won't open in Packet Tracer

**Possible causes:**
1. XML was edited incorrectly
2. Broken XML structure
3. Version incompatibility

**Test:**
```bash
# Check if XML is valid
xmllint network.xml

# Try converting a file without editing
./pka2xml -d original.pkt test.xml
./pka2xml -e test.xml test.pkt
# If test.pkt opens, the problem is in the editing
```

### Conversion is very slow

**Normal for:**
- Large files (>5MB)
- Complex topologies (>50 devices)

**If too slow (>30s):**
- Check disk space
- Close other programs
- Use SSD if possible

## Security and Privacy

### Is it safe to use this tool?

Yes! The tool:
- Is open source (you can audit it)
- Doesn't send data to internet
- Doesn't modify original files (only creates new ones)
- Uses trusted libraries (CryptoPP, RE2)

### Can I use it on confidential files?

Yes, everything is processed locally. But remember:
- Don't commit sensitive files to Git
- XMLs are plain text (visible)
- Keep backups of important files

## Advanced

### How does PKT encryption work?

Simplified:
1. **XOR**: Each byte is XORed with file size
2. **zlib**: Content is compressed
3. **Base64**: Some sections use Base64 encoding
4. **XML**: Final format is structured XML

Details: [Author's blog](https://mircodezorzi.github.io/doc/reversing-packet-tracer/)

### Can I contribute to the project?

Yes! See [CONTRIBUTING.md](CONTRIBUTING.md)

### Where to report bugs?

Open an issue on GitHub with:
- Problem description
- Steps to reproduce
- Operating system
- Packet Tracer version

## Still have questions?

1. 📖 Read [README.md](README.md)
2. 🚀 Check [QUICK_START.md](QUICK_START.md)
3. 💡 Explore [examples](examples/)
4. 🐛 Open an issue on GitHub

---

**Tip**: Use `Ctrl+F` (or `Cmd+F` on Mac) to search for your question in this file! 🔍
