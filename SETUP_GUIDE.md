# Universal Knowledge Assistant - Setup Guide

## 🚀 Quick Start (First-Time Setup)

### One-Click Setup
Just double-click **`launch_setup.bat`** or **`first_run_setup.pyw`** to start the guided setup wizard!

The wizard will:
1. ✅ Check if Ollama is installed and running
2. ✅ Install Python dependencies automatically
3. ✅ Download recommended AI model (if needed)
4. ✅ Configure your knowledge base path
5. ✅ Create desktop shortcut
6. ✅ Launch the application

**Setup takes less than 2 minutes!**

---

## 📋 Prerequisites

### Required
- **Python 3.8+** - [Download here](https://www.python.org/downloads/)
- **Ollama** - [Download here](https://ollama.ai)
  - After installing, run: `ollama pull qwen2.5-coder:3b`

### Optional
The setup wizard will install these automatically:
- `ollama` Python package
- `customtkinter` (modern GUI)
- `chromadb` (vector database)
- `sentence-transformers` (embeddings)
- `pyyaml`, `Pillow`

---

## 🎯 User Journey

### Step 1: Clone Repository
```bash
git clone <your-repo-url>
cd universal-knowledge-assistant
```

### Step 2: Run Setup Wizard
**Option A:** Double-click `launch_setup.bat`
**Option B:** Double-click `first_run_setup.pyw`

### Step 3: Follow Wizard Screens

#### Screen 1: Welcome
- Overview of features
- Privacy-first local AI
- One-click installation

#### Screen 2: Dependencies Check
- Auto-detects Ollama installation
- Shows available models
- One-click install missing packages
- One-click download recommended model

#### Screen 3: Configuration
- **Knowledge Base Path**: Select folder to index
  - Examples: `E:\Research-Papers`, `E:\Code-Projects`
- **Model Selection**: Choose from installed Ollama models
- **App Name**: Customize window title

#### Screen 4: Use Cases
Explore example configurations:
- 📚 Research Library
- ⚖️ Legal Documents
- 🏥 Medical Records
- 💻 Code Development
- 💼 Business Knowledge
- 📖 Personal Library

#### Screen 5: Finalization
- Review configuration summary
- Create desktop shortcut (optional)
- Launch app immediately (optional)
- Click **"Finish Setup"**

### Step 4: Use the App!
After setup completes, you'll find:
- Desktop shortcut: **"Universal Knowledge Assistant"**
- Configuration file: `config.yaml`
- Setup marker: `.setup_complete`

---

## 🔧 Manual Setup (Advanced)

If you prefer manual configuration:

1. **Copy config template:**
   ```bash
   copy config.yaml.example config.yaml
   ```

2. **Edit config.yaml:**
   ```yaml
   assistant:
     name: "Your App Name"
   
   models:
     default: "qwen2.5-coder:3b"
   
   codebase:
     path: "E:\\Your-Knowledge-Base"
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create shortcut (optional):**
   ```powershell
   powershell -ExecutionPolicy Bypass -File create_desktop_shortcut.ps1
   ```

5. **Launch:**
   ```bash
   launch_assistant.bat
   ```

---

## 🎨 File Structure

```
universal-knowledge-assistant/
├── first_run_setup.pyw          # Setup wizard GUI (MAIN ENTRY POINT)
├── setup_wizard.py              # Backend logic for wizard
├── launch_setup.bat             # Convenience launcher for wizard
├── launch_assistant.bat         # Main app launcher (checks for setup)
├── launch_assistant_gui.pyw     # GUI app (no console)
├── gui_assistant.py             # Main application
├── assistant_core.py            # Core assistant logic
├── indexed_assistant.py         # Fast indexed search
├── index_codebase.py            # Index builder
├── config.yaml.example          # Config template
├── config.yaml                  # User config (created by wizard)
├── .setup_complete              # Setup marker (created by wizard)
├── requirements.txt             # Python dependencies
└── assets/
    └── universal-knowledge/     # Logo and icons
        ├── LLM-Assistant-Logo.png
        ├── favicon.ico
        └── android-chrome-*.png
```

---

## 🔄 Reconfiguring

To change settings after initial setup:

**Option 1:** Run setup wizard again
```bash
launch_setup.bat
```

**Option 2:** Edit `config.yaml` manually
```bash
notepad config.yaml
```

**Option 3:** Delete `.setup_complete` to force first-run wizard
```bash
del .setup_complete
launch_assistant.bat
```

---

## 🛠️ Troubleshooting

### "Ollama not running"
1. Start Ollama: Open Ollama app or run `ollama serve`
2. Verify: Open browser to `http://localhost:11434`
3. Re-run setup wizard

### "No models detected"
1. Download a model: `ollama pull qwen2.5-coder:3b`
2. Verify: `ollama list`
3. Re-run setup wizard

### "Python package errors"
1. Update pip: `python -m pip install --upgrade pip`
2. Click "Install Missing Packages" in wizard
3. Or manually: `pip install -r requirements.txt`

### "Setup wizard won't launch"
1. Check Python version: `python --version` (need 3.8+)
2. Install CustomTkinter: `pip install customtkinter`
3. Run with console: `python first_run_setup.pyw`

### "Desktop shortcut not working"
1. Re-run shortcut script:
   ```powershell
   powershell -ExecutionPolicy Bypass -File create_desktop_shortcut.ps1
   ```
2. Or create manually pointing to `launch_assistant.bat`

---

## 📊 Recommended Models

| Model | Size | RAM | Use Case |
|-------|------|-----|----------|
| `qwen2.5-coder:1.5b` | 1.5GB | ~1GB | Fast, simple queries |
| `qwen2.5-coder:3b` ⭐ | 3GB | ~2GB | **Balanced (recommended)** |
| `qwen2.5-coder:7b` | 7GB | ~4GB | Complex, detailed analysis |
| `llama3.2:3b` | 3GB | ~2GB | General knowledge |
| `mistral:7b` | 7GB | ~4GB | Creative writing |

⭐ **Recommended**: `qwen2.5-coder:3b` - Best balance of speed and quality

---

## 🎓 Use Case Examples

### Research Library
```yaml
codebase:
  path: "E:\\Research-Papers"
```
Index: PDFs, papers, notes
Query: "What studies mention neural networks in 2023?"

### Code Development
```yaml
codebase:
  path: "E:\\MyProject-Code"
```
Index: Source code, docs, APIs
Query: "Find all authentication functions"

### Legal Documents
```yaml
codebase:
  path: "E:\\Legal-Files"
```
Index: Contracts, case files, briefs
Query: "Search for non-compete clauses"

---

## 🔒 Privacy & Security

- ✅ **100% Local** - No data sent to cloud
- ✅ **Offline AI** - Runs entirely on your machine
- ✅ **HIPAA-safe** - Suitable for medical records
- ✅ **No telemetry** - Zero tracking or analytics

---

## 📝 License

See [LICENSE](LICENSE) file for details.

---

## 🤝 Support

- Open an issue on GitHub
- Check troubleshooting section above
- Review `config.yaml.example` for configuration options

---

**Enjoy your Universal Knowledge Assistant! 🎉**
