# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## [1.0.0] - 2026-03-20

### ✨ Added

#### Main Features
- PKT/PKA to XML file conversion
- XML back to PKT conversion
- Support for Packet Tracer 7.x, 8.x, and 9.x
- Automatic build script (`build.sh`) for macOS and Linux

#### Documentation
- Complete README.md in English
- QUICK_START.md for quick start
- FAQ.md with frequently asked questions
- CONTRIBUTING.md with contribution guide
- Example documentation

#### Example Scripts
- `batch-convert.sh` - Batch conversion of multiple files
- `extract-info.sh` - Topology information extraction
- README.md with practical examples and student activities

#### Configuration Files
- `.gitignore` configured for C++ projects
- LICENSE (MIT)
- Organized directory structure

#### Example File
- `example.pkt` - Example file for testing

### 🔧 Technical

- Compilation with C++17 support
- Dependencies: CryptoPP, RE2, zlib
- Support for Apple Silicon (M1/M2) and Intel
- Automatic detection of Homebrew paths
- Descriptive error messages

### 📚 Educational

- Didactic examples for students
- Suggested activities in examples README
- Use cases for educators
- Automation scripts for exercise creation

---

## Roadmap (Planned)

### [1.1.0] - Future

#### Planned
- [ ] Native Windows support
- [ ] Graphical user interface (GUI)
- [ ] XML validation before converting to PKT
- [ ] Verbose mode with more debug information
- [ ] Optional XML compression
- [ ] Support for Packet Tracer 10.x (when released)

### [1.2.0] - Future

#### Planned
- [ ] Visual topology comparison tool
- [ ] PDF report generation
- [ ] Automatic network diagram extraction
- [ ] Topology validator (checks for errors)
- [ ] IOS configuration converter

### [2.0.0] - Future

#### Planned
- [ ] REST API for server-side conversion
- [ ] VSCode plugin
- [ ] Integration with Learning Management Systems (LMS)
- [ ] Support for other network simulators

---

## How to Contribute

See [CONTRIBUTING.md](CONTRIBUTING.md) to learn how to suggest features or report bugs.

---

## Entry Format

We use the following types of changes:

- `✨ Added` - For new features
- `🔧 Changed` - For changes to existing features
- `🗑️ Deprecated` - For features that will be removed
- `❌ Removed` - For removed features
- `🐛 Fixed` - For bug fixes
- `🔒 Security` - For security fixes

---

## References

This project is based on:
- [pka2xml](https://github.com/mircodz/pka2xml) by @mircodezorzi
- [ptexplorer](https://github.com/axcheron/ptexplorer) by @axcheron
