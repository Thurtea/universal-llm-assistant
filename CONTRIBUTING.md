# Contributing to Universal Knowledge Assistant

Thank you for your interest in contributing! We welcome contributions from the community to make this project even better.

## 🤝 How to Contribute

### Ways You Can Help

- 🐛 **Report Bugs** - Found an issue? Let us know!
- 💡 **Suggest Features** - Have an idea? We'd love to hear it!
- 📚 **Improve Documentation** - Help make our docs clearer
- 🔧 **Submit Code** - Fix bugs or add features
- ⭐ **Star the Repo** - Show your support!
- 💬 **Answer Questions** - Help other users in Discussions

## 🐛 Reporting Bugs

### Before Reporting
1. **Search existing issues** - Check if someone already reported it
2. **Try the latest version** - Bug might be fixed already
3. **Gather information** - Python version, OS, error messages

### Bug Report Template
```markdown
**Description:**
Clear description of the bug

**Steps to Reproduce:**
1. Launch the app
2. Click on...
3. Error appears

**Expected Behavior:**
What should happen instead

**Environment:**
- OS: Windows 11 / Ubuntu 22.04 / macOS 14
- Python Version: 3.11.5
- Ollama Version: 0.1.17
- App Version: 1.0.0

**Error Message:**
```
Paste full error message here
```

**Screenshots:**
If applicable, add screenshots
```

[Create Bug Report](https://github.com/yourusername/universal-knowledge-assistant/issues/new?labels=bug)

## 💡 Suggesting Features

We love new ideas! When suggesting features:

1. **Check existing suggestions** - Someone might have proposed it
2. **Explain the use case** - Why would this be useful?
3. **Describe the solution** - How should it work?
4. **Consider alternatives** - Are there other approaches?

### Feature Request Template
```markdown
**Problem:**
What problem does this solve?

**Proposed Solution:**
How should it work?

**Alternatives Considered:**
Other ways to solve this

**Use Case:**
Real-world scenario where this helps
```

[Suggest a Feature](https://github.com/yourusername/universal-knowledge-assistant/issues/new?labels=enhancement)

## 🔧 Pull Requests

### Getting Started

1. **Fork the repository**
   ```bash
   # Click "Fork" on GitHub, then clone your fork
   git clone https://github.com/YOUR_USERNAME/universal-knowledge-assistant.git
   cd universal-knowledge-assistant
   ```

2. **Create a branch**
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/bug-description
   ```

3. **Set up development environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

### Development Guidelines

#### Code Style
- **Python**: Follow [PEP 8](https://pep8.org/)
- **Docstrings**: Use triple-quoted strings for functions
- **Comments**: Explain *why*, not *what*
- **Naming**: Use descriptive variable names

```python
# Good
def calculate_semantic_similarity(query: str, document: str) -> float:
    """
    Calculate similarity between query and document using embeddings.
    
    Args:
        query: User's search query
        document: Document text to compare against
        
    Returns:
        Similarity score between 0.0 and 1.0
    """
    # Implementation here
    pass

# Avoid
def calc(q, d):  # Unclear naming
    x = something()  # No documentation
    return x
```

#### Testing
- **Test your changes** - Ensure nothing breaks
- **Add tests** - For new features when possible
- **Manual testing** - Run the GUI and verify behavior

```bash
# Run the app to test manually
python gui_assistant.py

# Run the setup wizard
python first_run_setup.pyw
```

#### Commits
- **Atomic commits** - One logical change per commit
- **Clear messages** - Describe what and why

```bash
# Good commit messages
git commit -m "Add support for PDF indexing in ChromaDB"
git commit -m "Fix: Resolve Ollama connection timeout on slow networks"
git commit -m "Docs: Update setup guide with macOS instructions"

# Avoid
git commit -m "fixes"
git commit -m "update stuff"
```

### Pull Request Process

1. **Update documentation** if needed
2. **Test thoroughly** on your system
3. **Push your branch**
   ```bash
   git push origin feature/your-feature-name
   ```

4. **Open Pull Request** on GitHub
   - Use a clear title
   - Reference related issues: "Fixes #123"
   - Describe your changes
   - Add screenshots for UI changes

5. **Respond to feedback**
   - Address review comments
   - Push additional commits if needed

6. **Merge** - Maintainers will merge when approved

### PR Template
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement

## Related Issues
Fixes #123

## Testing
- [ ] Tested on Windows
- [ ] Tested on Linux
- [ ] Tested on macOS
- [ ] Tested with setup wizard
- [ ] Tested with existing config

## Screenshots
If applicable, add screenshots

## Checklist
- [ ] Code follows project style
- [ ] Documentation updated
- [ ] No breaking changes (or documented)
- [ ] Tested locally
```

## 📚 Documentation

### Areas to Improve
- README.md - Main project documentation
- SETUP_GUIDE.md - Setup instructions
- QUICK_START.md - Quick reference
- Code comments and docstrings
- Wiki pages (if applicable)

### Documentation Style
- **Clear and concise** - Avoid jargon
- **Examples** - Show, don't just tell
- **Screenshots** - Visual aids help
- **Up-to-date** - Verify accuracy

## 🎨 UI/UX Contributions

### Design Guidelines
- **Dark theme consistency** - Match existing color palette
- **Accessibility** - Consider users with disabilities
- **Responsive** - Test different window sizes
- **Professional** - Clean, minimal design

### Color Palette
```python
BG_COLOR = "#0a0a0a"
PANEL_COLOR = "#111111"
INPUT_COLOR = "#151515"
BORDER_COLOR = "#262626"
TEXT_COLOR = "#f5f5f5"
MUTED_COLOR = "#9e9e9e"
ACCENT_COLOR = "#d4d4d4"
SUCCESS_COLOR = "#4ade80"
WARNING_COLOR = "#facc15"
ERROR_COLOR = "#f97373"
```

## 🌍 Internationalization

Future goal: Support multiple languages
- Keep strings separate from logic
- Use clear English in comments
- Consider RTL language support

## 📋 Project Structure

Understanding the codebase:

```
universal-knowledge-assistant/
├── first_run_setup.pyw      # Setup wizard GUI
├── setup_wizard.py          # Setup backend logic
├── gui_assistant.py         # Main application GUI
├── assistant_core.py        # Core LLM interaction
├── indexed_assistant.py     # ChromaDB vector search
├── index_codebase.py        # Indexing script
├── config.yaml.example      # Configuration template
└── assets/                  # Images and icons
```

### Key Files to Know
- **gui_assistant.py** - Main app interface and layout
- **assistant_core.py** - Ollama API interaction, query processing
- **indexed_assistant.py** - Vector search implementation
- **setup_wizard.py** - Setup wizard backend (dependency checks, config generation)
- **first_run_setup.pyw** - Setup wizard GUI screens

## 🚀 Release Process

For maintainers:

1. **Version bump** in relevant files
2. **Update CHANGELOG.md**
3. **Test thoroughly**
4. **Tag release**: `git tag v1.0.0`
5. **Push tag**: `git push origin v1.0.0`
6. **Create GitHub Release** with notes

## ❓ Questions?

- 💬 **Discussions**: [GitHub Discussions](https://github.com/yourusername/universal-knowledge-assistant/discussions)
- 🐛 **Issues**: [GitHub Issues](https://github.com/yourusername/universal-knowledge-assistant/issues)
- 📧 **Email**: For private inquiries

## 📜 Code of Conduct

### Our Standards

**Be:**
- ✅ Respectful and inclusive
- ✅ Constructive with feedback
- ✅ Patient with newcomers
- ✅ Professional in communication

**Don't:**
- ❌ Harass or discriminate
- ❌ Use offensive language
- ❌ Share others' private info
- ❌ Engage in trolling

### Enforcement
Violations may result in:
1. Warning
2. Temporary ban
3. Permanent ban

Report issues to: conduct@yourproject.com

## 🙏 Recognition

Contributors are recognized:
- In release notes
- In CONTRIBUTORS.md (if created)
- On the GitHub contributors page

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

**Thank you for making Universal Knowledge Assistant better!** 🎉

We appreciate every contribution, whether it's:
- A typo fix
- A bug report
- A feature suggestion
- A major new feature

Every bit helps make this project more useful for everyone! ❤️
