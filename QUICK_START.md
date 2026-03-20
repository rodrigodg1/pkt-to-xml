# 🚀 Quick Start Guide

This guide will help you get started with the tool in 5 minutes!

## 📦 Quick Installation

### macOS

```bash
# 1. Install dependencies
brew install cryptopp re2

# 2. Clone repository
git clone https://github.com/YOUR_USERNAME/pkt-to-xml-converter.git
cd pkt-to-xml-converter

# 3. Build
./build.sh

# 4. Done! Test it:
./pka2xml
```

### Linux (Ubuntu/Debian)

```bash
# 1. Install dependencies
sudo apt-get update
sudo apt-get install build-essential libcryptopp-dev libre2-dev zlib1g-dev git

# 2. Clone repository
git clone https://github.com/YOUR_USERNAME/pkt-to-xml-converter.git
cd pkt-to-xml-converter

# 3. Build
chmod +x build.sh
./build.sh

# 4. Done! Test it:
./pka2xml
```

## 💡 Basic Usage

### Convert PKT → XML

```bash
./pka2xml -d my_network.pkt my_network.xml
```

### Convert XML → PKT

```bash
./pka2xml -e my_network.xml new_network.pkt
```

## 📝 Common Use Cases

### 1️⃣ View network info without opening Packet Tracer

```bash
# Convert to XML
./pka2xml -d network.pkt network.xml

# View content
cat network.xml

# Or search for something specific
grep "Router" network.xml
```

### 2️⃣ Modify a topology

```bash
# 1. Convert to XML
./pka2xml -d original.pkt network.xml

# 2. Edit the XML (use nano, vim, VSCode, etc.)
nano network.xml

# 3. Convert back
./pka2xml -e network.xml modified.pkt

# 4. Open in Packet Tracer!
```

### 3️⃣ Compare two networks

```bash
./pka2xml -d network1.pkt network1.xml
./pka2xml -d network2.pkt network2.xml
diff network1.xml network2.xml
```

### 4️⃣ Extract device list

```bash
./pka2xml -d network.pkt network.xml
grep "<NAME" network.xml | grep -v translate
```

### 5️⃣ Count devices

```bash
./pka2xml -d network.pkt network.xml

# Count Routers
grep -c "Router" network.xml

# Count Switches
grep -c "Switch" network.xml

# Count PCs
grep -c "Pc" network.xml
```

## 🎓 For Teachers

### Automate exercise creation

```bash
# Create base template in XML
./pka2xml -d template.pkt template.xml

# Create variations using scripts
for i in {1..10}; do
    sed "s/LAB_NUMBER/$i/g" template.xml > lab_$i.xml
    ./pka2xml -e lab_$i.xml lab_$i.pkt
done
```

### Verify student work

```bash
# Script to check if a topology meets minimum requirements
./pka2xml -d student_work.pkt work.xml

routers=$(grep -c "Router" work.xml)
switches=$(grep -c "Switch" work.xml)

if [ $routers -ge 2 ] && [ $switches -ge 1 ]; then
    echo "✅ Topology meets requirements"
else
    echo "❌ Missing devices"
fi
```

## 🔧 Tips and Tricks

### Make the command global (optional)

```bash
# Copy to /usr/local/bin
sudo cp pka2xml /usr/local/bin/

# Now you can use it from anywhere:
pka2xml -d ~/Desktop/network.pkt ~/Desktop/network.xml
```

### Create an alias

Add to your `~/.bashrc` or `~/.zshrc`:

```bash
alias pkt2xml='~/pkt-to-xml-converter/pka2xml -d'
alias xml2pkt='~/pkt-to-xml-converter/pka2xml -e'
```

Then:
```bash
pkt2xml network.pkt network.xml
xml2pkt network.xml network.pkt
```

### Process multiple files

```bash
# Convert all .pkt files in a directory
for file in *.pkt; do
    ./pka2xml -d "$file" "${file%.pkt}.xml"
done
```

## ❓ Common Problems

### "command not found"
```bash
# Make sure to use ./
./pka2xml -d file.pkt output.xml

# Or add execute permission
chmod +x pka2xml
```

### "error opening input file"
```bash
# Check if file exists
ls -la file.pkt

# Use absolute path if needed
./pka2xml -d /full/path/file.pkt output.xml
```

### Compilation error
```bash
# Reinstall dependencies
# macOS:
brew reinstall cryptopp re2

# Linux:
sudo apt-get install --reinstall libcryptopp-dev libre2-dev
```

## 📚 Next Steps

1. ✅ Read the complete [README.md](README.md)
2. ✅ Explore the [examples](examples/)
3. ✅ Try modifying XMLs and converting back
4. ✅ Create your own automation scripts

## 🆘 Need Help?

- Check [README.md](README.md) for complete documentation
- See [practical examples](examples/)
- Open an issue on GitHub

---

**Final Tip**: Always keep a backup of your original `.pkt` files before modifying! 💾
