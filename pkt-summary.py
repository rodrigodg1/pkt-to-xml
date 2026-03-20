#!/usr/bin/env python3
"""
pkt-summary: Compact network topology extractor for Packet Tracer XML files.

Converts verbose Packet Tracer XML (often 500KB–2MB) into a focused
representation for LLM-based evaluation of student network designs.

Reduction ratios (typical):
  Full XML:       500 KB – 2 MB
  Stripped XML:   50–200 KB      (~10x reduction,  preserves full config)
  JSON summary:   5–30 KB        (~50–100x reduction, ideal for LLM input)

Usage:
  # JSON summary (default) — most compact, ideal for LLM evaluation
  python3 pkt-summary.py network.xml

  # Stripped XML — removes visual bloat, keeps full network config detail
  python3 pkt-summary.py network.xml --strip

  # Work directly from .pkt file (requires pka2xml binary)
  python3 pkt-summary.py network.pkt --pka2xml ./pka2xml

  # Save to file and see size statistics
  python3 pkt-summary.py network.xml -o summary.json
  python3 pkt-summary.py network.xml --strip -o compact.xml
"""

import argparse
import json
import os
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
from typing import Optional

# ── SECTIONS REMOVED AT ROOT LEVEL ────────────────────────────────────────────
# These sections contain only visual/UI data with zero networking value.
ROOT_STRIP = {
    "PHYSICALWORKSPACE",    # Physical 3D workspace layout     (~70% of file)
    "OPTIONS",              # UI fonts, colors, grid settings  (~10% of file)
    "SCENARIOSET",          # Simulation scenarios
    "PIXMAPBANK",           # Embedded graphics
    "MOVIEBANK",            # Animations
    "GEOVIEW_GRAPHICSITEMS",# Geographic view decorations
    "ELLIPSES",
    "LINES",
    "POLYGONS",
    "RECTANGLES",
    "SCRIPT_MODULE",
    "CLUSTERS",
    "CODE_TESTING",
    "COMMAND_LOGS",
    "EXT_PORT_MGR",
    "CEPS",
    "USER_PROFILE",
    "MULTIUSER",
    "FILTERS",
}

# ── ENGINE-LEVEL BLOAT REMOVED FROM EACH DEVICE ───────────────────────────────
ENGINE_STRIP = {
    "FILE_MANAGER",           # Server filesystem content (HTML/FTP files, often 50 KB+)
    "WIRELESS_CLIENT",
    "CELLULAR_CLIENT",
    "EMAIL_CLIENT",
    "EMAIL_SERVER",
    "FTP_SERVER",
    "HTTP_SERVER",
    "HTTPS_SERVER",
    "TFTP_SERVER",
    "TERMINAL_SETTINGS",
    "LOCK_SETTINGS",
    "IMAGE_SETTINGS",
    "PPPOE_SETTINGS",
    "USER_APPS",
    "IOX_SEVICE",
    "IOX_VM_MANAGER",
    "IOE_USER_MANAGER",
    "EAP_METHODS",
    "PTP_PROCESS",
    "COORD_SETTINGS",
    "CUSTOM_VARS",
    "CUSTOM_INTERFACE",
    "VOIP_TFTP_IP",
    "GUI_TAB",
    "HTML_TAB",
    "TRAFFICGEN_USER_TRAFFIC",
    "REGISTRATION_SEVER",
    "NF_COLLECTOR",
    "ACS_SERVER",
    "SNMP_MANAGER",
    "EXT_ATTRIBUTES",
    "USB_PORT_COUNT",
    "TEMPLATE_CREATION_TIME",
    "IGNORE_TEMPLATE_CREATION_TIME",
    "IGNORED_VERSION",
    "PTP_ENALBED",
    "POWER",
    "DOT1X_SETTINGS",
    "SCRIPT_DATA_STORES",
    "RUNNING_APPS",
    "STARTSIMTIME",
    "STARTTIME",
    "SERIALNUMBER",
    "SCRIPT_MODULE_DATA",
    "PHYSICAL_CPUR",
    "NDV6",                   # IPv6 neighbor discovery (large, rarely evaluated)
}

# ── VISUAL / POSITIONAL TAGS REMOVED FROM ALL LEVELS ──────────────────────────
VISUAL_STRIP = {
    "SX", "SY",
    "INIT_DEPTH", "INIT_HEIGHT", "INIT_SX", "INIT_SY", "INIT_SZ", "INIT_WIDTH",
    "ICP_CSX", "ICP_CSY",
    "SCALE_FACTOR", "SCALED_PIXMAP_HEIGHT", "SCALED_PIXMAP_WIDTH",
    "CUSTOM_IMAGE_HEIGHT", "CUSTOM_IMAGE_WIDTH",
    "MANUAL_SCALING",
    "X_COORD", "Y_COORD", "Z_COORD", "X_PN", "Y_PN",
    "GEO_VIEW_COLOR",
    "IS_MANAGED_IN_RACK_VIEW",
    "LENGTH",                 # Cable length in the diagram (visual only)
    "FROM_DEVICE_MEM_ADDR", "TO_DEVICE_MEM_ADDR",
    "FROM_PORT_MEM_ADDR", "TO_PORT_MEM_ADDR",
    "BG_TILED",
}

# ── PORT-LEVEL PHYSICAL HARDWARE DETAILS REMOVED ──────────────────────────────
PORT_STRIP = {
    "COVERAGERANGE",          # Wireless coverage radius (visual)
    "SAVED_FULLDUPLEX",
    "FIBERMULTIMODE",
    "MEDIATYPE",
    "PINS",
    "TIMEOUT",
    "AUTONEGOTIATEBANDWIDTH",
    "AUTONEGOTIATEDUPLEX",
    "AUTONEGOTIATESPEED",
    "CHANNEL", "CHANNEL5GHZ",
    "PC_FIREWALL", "PC_IPV6_FIREWALL",
    "ND_SUPPRESSED",
    "ND_IPV6_DNS_ADDRESSES",
    "IPV6_ENABLED",
    "IPV6_ADDRESS_AUTOCONFIG",
    "IPV6_DEFAULT_LINK_LOCAL",
    "IPV6_PORT_DHCP_ENABLED",
    "IPV6_ADDRESSES",
    "IP_UNNUMBERED",
    "DHCP_SERVER_IP",
}

# ── IoT / ANIMATION DATA REMOVED ──────────────────────────────────────────────
# These tags generate hundreds of repeated identical entries per IoT sensor.
IOT_ANIM_STRIP = {
    "ENVIRONMENT",
    "ENVIRONMENT_OPTIONS",
    "ENVIRONMENT_OPTION",
    "KEYFRAMES",
    "KEYFRAME",
    "ANIMATION",
}


# ══ UTILITY ═══════════════════════════════════════════════════════════════════

def _prune(el: ET.Element, tags: set) -> None:
    """Recursively remove all direct children matching the given tag set."""
    to_remove = [c for c in el if c.tag in tags]
    for c in to_remove:
        el.remove(c)
    for c in list(el):
        _prune(c, tags)


# ══ STRIP MODE ════════════════════════════════════════════════════════════════

def strip_xml(root: ET.Element) -> ET.Element:
    """
    Remove non-essential elements from the XML tree (in-place).

    Typical result: ~10x smaller than the original XML while preserving
    all networking configuration (IPs, routing, VLANs, ACLs, DHCP, etc.).
    """
    # 1. Root-level visual sections
    _prune(root, ROOT_STRIP)

    # 2. Per-device: remove visual WORKSPACE entirely
    for device in root.findall(".//DEVICE"):
        for ws in list(device.findall("WORKSPACE")):
            device.remove(ws)

    # 3. Per-device ENGINE: remove non-network bloat
    for engine in root.findall(".//ENGINE"):
        _prune(engine, ENGINE_STRIP)
        # Also clean up the SAVE_REF_ID (memory address reference, not needed)
        for ref in list(engine.findall("SAVE_REF_ID")):
            engine.remove(ref)

    # 4. Port physical hardware details
    for port in root.findall(".//PORT"):
        _prune(port, PORT_STRIP)

    # 5. IoT / animation data (produces hundreds of identical tags)
    _prune(root, IOT_ANIM_STRIP)

    # 6. Visual / positional tags at all levels
    _prune(root, VISUAL_STRIP)

    return root


# ══ JSON SUMMARY MODE ═════════════════════════════════════════════════════════

def _txt(el: ET.Element, path: str, default: str = "") -> str:
    t = el.findtext(path, default)
    return (t or "").strip()


def _extract_port_config(port_el: ET.Element) -> dict:
    """Extract the networking configuration of a single PORT element."""
    p = {
        "mac":        _txt(port_el, "BIA") or _txt(port_el, "MACADDRESS"),
        "ip":         _txt(port_el, "IP"),
        "mask":       _txt(port_el, "SUBNET"),
        "enabled":    _txt(port_el, "ENABLED", "true").lower() == "true",
        "description":_txt(port_el, "DESCRIPTION"),
        "speed_mbps": _txt(port_el, "SPEED"),
        "bandwidth":  _txt(port_el, "BANDWIDTH"),
        "full_duplex":_txt(port_el, "FULLDUPLEX", "true").lower() == "true",
        "acl_in":     _txt(port_el, "ACL_IN_ID"),
        "acl_out":    _txt(port_el, "ACL_OUT_ID"),
        "vlan":       _txt(port_el, "VLAN"),
        "dhcp":       _txt(port_el, "PORT_DHCP_ENABLE", "false").lower() == "true",
        "gateway":    _txt(port_el, "PORT_GATEWAY"),
        "dns":        _txt(port_el, "PORT_DNS"),
        "clockrate":  _txt(port_el, "CLOCKRATE"),
        "type":       _txt(port_el, "TYPE"),
        "ssid":       _txt(port_el, "SSID"),
        "ipv6_link_local": _txt(port_el, "IPV6_LINK_LOCAL"),
    }
    # Keep only non-empty and non-default values to reduce noise
    skip = {"", None}
    result = {k: v for k, v in p.items()
              if v not in skip and v is not False and v != "0"}
    # Always keep ip/mask even if empty (helps LLM see unconfigured ports)
    if "ip" not in result:
        result["ip"] = ""
    return result


def _extract_interfaces(engine_el: ET.Element) -> list:
    """
    Extract all interface configurations from a device ENGINE.
    Returns list of dicts, each with the port config.
    """
    ports = []
    # Walk the nested MODULE/SLOT/MODULE/PORT structure
    for module in engine_el.findall(".//MODULE"):
        model = _txt(module, "MODEL")
        for port_el in module.findall("PORT"):
            cfg = _extract_port_config(port_el)
            cfg["_module_model"] = model
            ports.append(cfg)
    return ports


def _extract_dhcp_pools(engine_el: ET.Element) -> list:
    pools = []
    for pool in engine_el.findall(".//POOL"):
        p = {
            "name":       _txt(pool, "NAME"),
            "network":    _txt(pool, "NETWORK"),
            "mask":       _txt(pool, "MASK"),
            "start_ip":   _txt(pool, "START_IP"),
            "end_ip":     _txt(pool, "END_IP"),
            "gateway":    _txt(pool, "DEFAULT_ROUTER"),
            "dns_server": _txt(pool, "DNS_SERVER"),
            "domain":     _txt(pool, "DOMAIN_NAME"),
            "lease_time": _txt(pool, "LEASE_TIME"),
        }
        pools.append({k: v for k, v in p.items() if v})
    return pools


def _extract_acls(engine_el: ET.Element) -> list:
    acls = []
    for acl in engine_el.findall(".//ACL"):
        a: dict = {
            "id":   acl.get("id") or _txt(acl, "ID"),
            "name": _txt(acl, "NAME"),
            "type": _txt(acl, "TYPE"),
        }
        entries = []
        for stmt in acl.findall(".//STATEMENT"):
            text = _txt(stmt, "TEXT")
            if text:
                entries.append(text)
        if entries:
            a["entries"] = entries
        acls.append({k: v for k, v in a.items() if v})
    return acls


def _extract_device(dev_el: ET.Element) -> Optional[dict]:
    engine = dev_el.find("ENGINE")
    if engine is None:
        return None

    type_el = engine.find("TYPE")
    dtype  = (type_el.text or "").strip() if type_el is not None else ""
    model  = (type_el.get("model") or "").strip() if type_el is not None else ""
    name   = _txt(engine, "NAME")
    ref_id = _txt(engine, "SAVE_REF_ID")

    dev: dict = {
        "name":         name,
        "type":         dtype,
        "model":        model,
        "_save_ref_id": ref_id,   # used for link resolution, hidden with _
    }

    gateway = _txt(engine, "GATEWAY")
    if gateway:
        dev["gateway"] = gateway

    dns_client = engine.find("DNS_CLIENT")
    if dns_client is not None:
        servers = [_txt(s, "IP") for s in dns_client.findall(".//SERVER")]
        servers = [s for s in servers if s]
        if servers:
            dev["dns_servers"] = servers

    interfaces = _extract_interfaces(engine)
    if interfaces:
        dev["interfaces"] = interfaces

    dhcp_pools = _extract_dhcp_pools(engine)
    if dhcp_pools:
        dev["dhcp_pools"] = dhcp_pools

    acls = _extract_acls(engine)
    if acls:
        dev["acls"] = acls

    desc = _txt(engine, "DESCRIPTION")
    if desc:
        dev["description"] = desc

    return dev


def _build_ref_map(root: ET.Element) -> dict:
    """Map 'save-ref-id:<N>' strings to device names."""
    ref_map = {}
    for engine in root.findall(".//ENGINE"):
        ref = _txt(engine, "SAVE_REF_ID")
        name = _txt(engine, "NAME")
        if ref and name:
            ref_map[f"save-ref-id:{ref}"] = name
    return ref_map


def _extract_connections(root: ET.Element, ref_map: dict) -> list:
    """Extract cable connections with human-readable device names."""
    connections = []
    for link in root.findall(".//LINK"):
        cable = link.find("CABLE")
        if cable is None:
            continue

        link_type  = _txt(link,  "TYPE")
        cable_type = _txt(cable, "TYPE")
        from_ref   = _txt(cable, "FROM")
        to_ref     = _txt(cable, "TO")
        functional = _txt(cable, "FUNCTIONAL", "true").lower() == "true"

        # CABLE contains exactly 2 <PORT> children (one for each endpoint)
        port_els = cable.findall("PORT")
        from_port = port_els[0].text.strip() if len(port_els) > 0 and port_els[0].text else ""
        to_port   = port_els[1].text.strip() if len(port_els) > 1 and port_els[1].text else ""

        conn = {
            "from_device": ref_map.get(from_ref, from_ref),
            "from_port":   from_port,
            "to_device":   ref_map.get(to_ref, to_ref),
            "to_port":     to_port,
            "cable_type":  cable_type or link_type,
        }
        if not functional:
            conn["down"] = True
        connections.append(conn)
    return connections


def make_json_summary(root: ET.Element) -> dict:
    """
    Build a compact JSON network topology summary from the parsed XML root.

    The output focuses exclusively on what matters for evaluating a
    network design:
      - Device inventory (name, type, model)
      - Interface configurations (IP, mask, enabled state, ACLs, VLANs)
      - Default gateways and DNS servers
      - DHCP pool configurations
      - Access Control Lists
      - Cable/link connections (with endpoint device names and port names)
      - IP address summary table
    """
    version = (root.findtext("VERSION") or "").strip()
    ref_map = _build_ref_map(root)

    devices = []
    for dev_el in root.findall(".//DEVICE"):
        d = _extract_device(dev_el)
        if d:
            devices.append(d)

    connections = _extract_connections(root, ref_map)

    # Build a flat address table for quick LLM overview
    address_summary = []
    for d in devices:
        for iface in d.get("interfaces", []):
            ip = iface.get("ip", "")
            if ip and ip != "0.0.0.0":
                address_summary.append({
                    "device":  d["name"],
                    "ip":      ip,
                    "mask":    iface.get("mask", ""),
                    "gateway": d.get("gateway", ""),
                })

    # Remove internal _save_ref_id before serialising
    for d in devices:
        d.pop("_save_ref_id", None)

    return {
        "pt_version":      version,
        "device_count":    len(devices),
        "connection_count": len(connections),
        "devices":         devices,
        "connections":     connections,
        "address_summary": address_summary,
    }


# ══ PKT DIRECT INPUT SUPPORT ══════════════════════════════════════════════════

def pkt_to_xml_string(pkt_file: str, pka2xml_path: str) -> str:
    """Convert a .pkt/.pka file to XML string using the pka2xml binary."""
    with tempfile.NamedTemporaryFile(suffix=".xml", delete=False) as f:
        tmp_xml = f.name
    try:
        result = subprocess.run(
            [pka2xml_path, "-d", pkt_file, tmp_xml],
            capture_output=True, text=True,
        )
        if result.returncode != 0:
            sys.exit(f"Error: pka2xml failed:\n{result.stderr.strip()}")
        with open(tmp_xml, encoding="utf-8", errors="replace") as f:
            return f.read()
    finally:
        if os.path.exists(tmp_xml):
            os.unlink(tmp_xml)


# ══ MAIN ══════════════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(
        description=(
            "Extract a compact network topology from a Packet Tracer XML file "
            "for use as LLM input when evaluating student network designs."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "input",
        help="Input file: .xml (from pka2xml -d) or .pkt/.pka (requires --pka2xml)",
    )
    parser.add_argument(
        "--strip",
        action="store_true",
        help=(
            "Output a stripped XML instead of a JSON summary. "
            "Removes all visual/UI bloat but keeps full network config detail. "
            "The result can still be re-encrypted back to .pkt with pka2xml -e."
        ),
    )
    parser.add_argument(
        "-o", "--output",
        default="-",
        help="Output file path. Use '-' for stdout (default).",
    )
    parser.add_argument(
        "--pka2xml",
        default="./pka2xml",
        help="Path to the pka2xml binary (only needed for .pkt/.pka input).",
    )
    parser.add_argument(
        "--indent",
        type=int,
        default=2,
        help="JSON indentation spaces. Use 0 for compact single-line output (default: 2).",
    )
    args = parser.parse_args()

    # ── Load input ────────────────────────────────────────────────────────────
    if args.input.lower().endswith((".pkt", ".pka")):
        xml_content = pkt_to_xml_string(args.input, args.pka2xml)
        root = ET.fromstring(xml_content)
        orig_size = os.path.getsize(args.input)
    else:
        tree = ET.parse(args.input)
        root = tree.getroot()
        orig_size = os.path.getsize(args.input)

    # ── Process ───────────────────────────────────────────────────────────────
    if args.strip:
        strip_xml(root)
        ET.indent(root, space="  ")
        output = ET.tostring(root, encoding="unicode")
        ext = ".xml"
    else:
        summary = make_json_summary(root)
        indent = args.indent if args.indent > 0 else None
        output = json.dumps(summary, indent=indent, ensure_ascii=False)
        ext = ".json"

    # ── Write output ──────────────────────────────────────────────────────────
    if args.output == "-":
        print(output)
    else:
        out_path = args.output
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(output)
        out_size = os.path.getsize(out_path)
        ratio = int(100 * out_size / orig_size) if orig_size else 0
        mode  = "stripped XML" if args.strip else "JSON summary"
        print(
            f"[pkt-summary] {mode}: {out_path}\n"
            f"  Input:  {orig_size:>10,} bytes\n"
            f"  Output: {out_size:>10,} bytes  ({ratio}% of input, "
            f"{orig_size // max(out_size,1)}x smaller)",
            file=sys.stderr,
        )


if __name__ == "__main__":
    main()
