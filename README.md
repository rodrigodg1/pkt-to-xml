# PKT to XML Converter

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Convert Cisco Packet Tracer files (`.pkt` / `.pka`) to XML and back. Supports Packet Tracer 7.x, 8.x, and 9.x.

---

## Installation

**macOS**
```bash
brew install cryptopp re2
./build.sh
```

**Linux (Ubuntu/Debian)**
```bash
sudo apt-get install build-essential g++ libcryptopp-dev libre2-dev zlib1g-dev
./build.sh
```

---

## Usage

### pka2xml — convert PKT ↔ XML

```bash
# Decrypt .pkt to XML
./pka2xml -d input.pkt output.xml

# Encrypt XML back to .pkt
./pka2xml -e input.xml output.pkt

# Fix cross-version compatibility
./pka2xml -f input.pkt output.pkt
```

### pkt-summary.py — inspect without opening Packet Tracer

Three output modes, all accepting `.pkt`, `.pka`, or a pre-decoded `.xml`:

| Mode | Flag | Output | Size vs full XML |
|------|------|--------|-----------------|
| JSON summary | *(default)* | devices, IPs, cables, IOS config | ~100–2000x smaller |
| Topology XML | `--topo` | concise XML with only configured data | ~100x smaller |
| Lean XML | `--strip` | full XML minus UI state / animations | ~10x smaller |

```bash
# JSON summary (stdout)
python3 pkt-summary.py examples/example.pkt

# Topology XML (stdout)
python3 pkt-summary.py examples/example.pkt --topo

# Lean XML saved to file
python3 pkt-summary.py examples/example.pkt --strip -o slim.xml
```

**When to use each tool:**

| `pka2xml -d` | `pkt-summary.py` |
|---|---|
| Need to edit XML and re-encrypt | Only reading / inspecting the topology |
| Need every field, including binary blobs | Need devices, IPs, cables, IOS config |

---

## Output examples

**JSON summary**
```bash
python3 pkt-summary.py examples/example.pkt
```
```json
{
  "file": "example.pkt",
  "version": "9.0.0.0810",
  "counts": { "Router": 2, "Switch": 3, "Pc": 5 },
  "devices": [
    {
      "name": "Router0",
      "type": "Router",
      "model": "1841",
      "interfaces": [
        { "name": "FastEthernet0/0", "ip": "192.168.1.1", "mask": "255.255.255.0", "status": "up" },
        { "name": "FastEthernet0/1", "ip": "10.0.0.1",    "mask": "255.255.255.252" }
      ],
      "config_preview": [
        "hostname Router0",
        "interface FastEthernet0/0",
        " ip address 192.168.1.1 255.255.255.0",
        " no shutdown"
      ]
    }
  ],
  "cables": [
    { "from": "Router0/FastEthernet0/0", "to": "Switch0/FastEthernet0/1", "type": "Straight-Through" }
  ]
}
```

**Topology XML**
```bash
python3 pkt-summary.py examples/example.pkt --topo
```
```xml
<?xml version="1.0" encoding="UTF-8"?>
<TOPOLOGY version="9.0.0.0810">
  <DEVICES>
    <DEVICE name="Router0" type="Router" model="1841">
      <INTERFACE name="FastEthernet0/0" ip="192.168.1.1" mask="255.255.255.0" status="up"/>
      <INTERFACE name="FastEthernet0/1" ip="10.0.0.1" mask="255.255.255.252"/>
      <CONFIG>
hostname Router0
interface FastEthernet0/0
 ip address 192.168.1.1 255.255.255.0
 no shutdown
      </CONFIG>
    </DEVICE>
    <DEVICE name="Switch0" type="Switch" model="2960-24TT"/>
    <DEVICE name="PC0" type="Pc" model="PC-PT">
      <INTERFACE name="FastEthernet0" ip="192.168.1.2" mask="255.255.255.0" status="up"/>
    </DEVICE>
  </DEVICES>
  <CABLES>
    <CABLE from="Router0/FastEthernet0/0" to="Switch0/FastEthernet0/1" type="Straight-Through"/>
    <CABLE from="PC0/FastEthernet0" to="Switch0/FastEthernet0/2" type="Straight-Through"/>
  </CABLES>
</TOPOLOGY>
```

**Save to file** — prints size reduction ratio:
```bash
python3 pkt-summary.py examples/example.pkt           -o summary.json
# Saved JSON summary to summary.json
# Size: 789,598 bytes -> 482 bytes  (1638.2x smaller)

python3 pkt-summary.py examples/example.pkt --topo    -o topo.xml
python3 pkt-summary.py examples/example.pkt --strip   -o slim.xml
```

---

## Troubleshooting

**`command not found: pka2xml`** — add execute permission:
```bash
chmod +x pka2xml
```

**`cryptopp/base64.h not found`** — reinstall dependencies:
```bash
# macOS
brew install cryptopp re2

# Linux
sudo apt-get install libcryptopp-dev libre2-dev zlib1g-dev
```

**`C++ versions less than C++17 are not supported`** — update compiler:
```bash
# macOS
xcode-select --install

# Linux
sudo apt-get install g++-9
```

---

## License

MIT — see [LICENSE](LICENSE).
Based on [pka2xml](https://github.com/mircodz/pka2xml) by [@mircodezorzi](https://github.com/mircodezorzi).
