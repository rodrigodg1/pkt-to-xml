# 🤝 Contributing Guide

Thank you for considering contributing to this project! This is an educational project and all help is welcome.

## 📋 How to Contribute

### 🐛 Report Bugs

If you found a bug, please open an issue including:

1. **Clear problem description**
2. **Steps to reproduce**
3. **Expected vs. actual behavior**
4. **Operating system and version**
5. **Packet Tracer version (if applicable)**
6. **Complete error messages**

**Example:**
```
### Description
Conversion fails when processing PT 9.x files

### Steps to reproduce
1. Run: ./pka2xml -d network.pkt network.xml
2. Use file created in PT 9.0

### Error
error opening input file

### System
- OS: Ubuntu 22.04
- PT Version: 9.0.0.0810
```

### 💡 Suggest Improvements

Open an issue with the "enhancement" label including:

1. Feature description
2. Use case
3. Benefits for users/students

### 🔧 Contribute Code

1. **Fork the repository**

2. **Clone your fork**
```bash
git clone https://github.com/YOUR_USERNAME/pkt-to-xml-converter.git
cd pkt-to-xml-converter
```

3. **Create a branch**
```bash
git checkout -b feature/my-contribution
```

4. **Make your changes**
   - Keep code clean and commented
   - Follow existing style
   - Test your changes

5. **Commit your changes**
```bash
git add .
git commit -m "Add feature X"
```

6. **Push to your fork**
```bash
git push origin feature/my-contribution
```

7. **Open a Pull Request**
   - Describe your changes
   - Reference related issues
   - Explain why the change is useful

## 📝 Code Guidelines

### C++ Code

- Use C++17
- Comment complex code
- Keep functions small and focused
- Prefer clarity over cleverness

### Shell Scripts

- Use `#!/bin/bash` at the beginning
- Add explanatory comments
- Validate user inputs
- Provide clear error messages

### Documentation

- Use clear and simple language
- Include practical examples
- Keep in English for wider audience
- Use emojis moderately for readability

## 🧪 Testing

Before submitting a PR, test:

1. **Compilation**
```bash
./build.sh
```

2. **PKT → XML Conversion**
```bash
./pka2xml -d test.pkt test.xml
```

3. **XML → PKT Conversion**
```bash
./pka2xml -e test.xml test_new.pkt
```

4. **Validation** (open generated .pkt in Packet Tracer)

## 📚 Areas that Need Help

- 📖 **Documentation**: Tutorials, examples, translations
- 🐛 **Testing**: Test with different PT versions
- 💻 **Scripts**: Useful scripts to automate tasks
- 🎨 **UI**: Graphical interface (future)
- 🔍 **Analysis**: Tools to analyze topologies

## 🎓 For Students

This is a great project to:
- Learn Git/GitHub
- Contribute to open source
- Practice C++
- Learn about reverse engineering
- Help other students

**Tip**: Start with small contributions:
- Fix typos in documentation
- Add examples
- Improve error messages
- Create useful scripts

## 🌟 Best Practices

### Commits

Use clear messages:
```
✅ Good: "Add support for Packet Tracer 9.x"
❌ Bad: "fix"

✅ Good: "Fix compilation error on Ubuntu 22.04"
❌ Bad: "update"
```

### Pull Requests

- One PR per feature
- Describe what changed and why
- Add screenshots if relevant
- Reference issues: "Fixes #123"

## 📄 License

By contributing, you agree that your contributions will be licensed under the same MIT License as the project.

## 🙋 Questions?

- Open an issue with the "question" tag
- Be specific in your question
- Include relevant context

## 🎯 Code of Conduct

- Be respectful and professional
- Accept constructive feedback
- Focus on what's best for the community
- Be patient with beginners

---

**Remember**: No contribution is too small! All help is valuable. 💚
