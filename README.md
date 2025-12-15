# Universal Knowledge Assistant

<div align="center">

![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg)
![Ollama](https://img.shields.io/badge/Ollama-Local%20AI-orange.svg)

**Index and query any knowledge base locally using AI**

*Privacy-first • No cloud required • Professional desktop application*

[Quick Start](#-quick-start) • [Features](#-features) • [Documentation](#-documentation) • [Use Cases](#-use-cases)

</div>

---

##  Quick Start

### **Zero-Terminal Setup (Recommended)**

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/universal-knowledge-assistant.git
   cd universal-knowledge-assistant
   ```

2. **Double-click `first_run_setup.pyw`** (or `launch_setup.bat`)

3. **Follow the 5-screen guided wizard** (takes less than 2 minutes)

4. **Done!** A desktop shortcut will be created. Click it to launch.

**That's it!** No terminal commands, no manual config editing, no confusion.

>  **New to this?** See [QUICK_START.md](QUICK_START.md) for the simplest instructions  
>  **Need details?** See [SETUP_GUIDE.md](SETUP_GUIDE.md) for comprehensive documentation

---

##  Features

###  **Privacy & Security**
-  **100% Local Processing** - All AI runs on your machine (no cloud, no API keys)
-  **HIPAA-Safe** - Suitable for medical records, legal docs, confidential data
-  **No Telemetry** - Zero tracking, zero analytics, zero data collection

###  **AI-Powered Search**
-  **Natural Language Queries** - Ask questions like "Find research on neural networks from 2023"
-  **Semantic Search** - ChromaDB vector database for intelligent document retrieval
-  **Multiple AI Models** - Switch between fast (1.5B), balanced (3B), or powerful (7B) models
-  **Context-Aware** - Add specific files for targeted deep-dive analysis

###  **Professional Desktop App**
-  **Modern Dark UI** - Clean, minimal interface inspired by professional tools
-  **Split-Panel Design** - Side-by-side query and response display
-  **One-Click Setup** - Guided wizard handles everything automatically
-  **Desktop Shortcut** - Launch like any native Windows application
-  **Copy/Paste Support** - Full keyboard shortcuts and context menus

###  **Performance**
-  **Fast Indexing** - ChromaDB creates searchable embeddings of your knowledge base
-  **10-100x Faster Queries** - Vector search vs. linear file scanning
-  **Multi-Format Support** - PDFs, code, text, markdown, and more
-  **Efficient Memory** - Models from 1GB to 4GB RAM usage

---

##  Use Cases

| Use Case | Description | Example Query |
|----------|-------------|---------------|
|  **Research Library** | Index academic papers, PDFs, notes | "What studies mention climate change mitigation?" |
|  **Legal Documents** | Search contracts, case files, briefs | "Find all non-compete clauses in contracts" |
|  **Medical Records** | Query patient notes (HIPAA-safe) | "Show patient history for diabetes cases" |
|  **Code Development** | Index codebases, APIs, design docs | "How does the authentication system work?" |
|  **Business Knowledge** | Search meeting notes, reports, docs | "What were Q3 revenue projections?" |
|  **Personal Library** | Books, articles, personal notes | "Find notes about productivity techniques" |

---

##  Requirements

### **System Requirements**
- **Python 3.8+** - [Download](https://www.python.org/downloads/)
- **Ollama** - [Download](https://ollama.ai) (local AI runtime)
- **2-8GB RAM** - Depends on selected model size
- **Windows / Linux / macOS** - Cross-platform support

### **Python Dependencies** (Auto-installed by wizard)
The setup wizard installs these automatically:
```
ollama>=0.1.0
pyyaml>=6.0
customtkinter>=5.0.0
Pillow>=10.0.0
chromadb>=0.4.0
sentence-transformers>=2.2.0
```

---

##  Project Structure

```
universal-knowledge-assistant/
 first_run_setup.pyw          #  START HERE - Setup wizard
 setup_wizard.py              # Backend logic for setup
 launch_assistant.bat         # Main app launcher
 gui_assistant.py             # GUI application
 assistant_core.py            # Core AI logic
 indexed_assistant.py         # Fast vector search
 index_codebase.py            # Knowledge base indexer
 config.yaml.example          # Configuration template
 requirements.txt             # Python dependencies
 QUICK_START.md               # 1-page quick reference
 SETUP_GUIDE.md               # Comprehensive setup docs
 assets/                      # Logo and icons
     universal-knowledge/
         LLM-Assistant-Logo.png
         favicon.ico
```

---

##  Advanced Usage

### **Manual Configuration**

If you prefer manual setup instead of the wizard:

```bash
# Copy config template
cp config.yaml.example config.yaml

# Edit configuration
notepad config.yaml

# Install dependencies
pip install -r requirements.txt

# Download Ollama model
ollama pull qwen2.5-coder:3b

# Launch app
python gui_assistant.py
```

### **Python API**

Use the assistant programmatically:

```python
from assistant_core import LLMAssistant

# Initialize
assistant = LLMAssistant(
    model="qwen2.5-coder:3b",
    codebase_path="E:\\My-Knowledge-Base",
    context_window=16384
)

# Query with context
response = assistant.query(
    "Summarize research on renewable energy",
    files=["research/solar.pdf", "research/wind.pdf"]
)
print(response)
```

### **Vector Indexing**

For 10-100x faster queries, create a vector index:

```bash
python index_codebase.py
```

This creates a `chroma_db/` directory with semantic embeddings. The GUI automatically uses the index when available.

---

##  Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

**Ways to contribute:**
-  Report bugs via [GitHub Issues](https://github.com/yourusername/universal-knowledge-assistant/issues)
-  Suggest features or improvements
-  Submit pull requests
-  Improve documentation
-  Star the repo if you find it useful!

---

##  License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

**Copyright © 2025**

---

##  Credits & Acknowledgments

Built with exceptional open-source tools:

- [**Ollama**](https://ollama.ai/) - Local LLM inference engine
- [**ChromaDB**](https://www.trychroma.com/) - Vector database for semantic search
- [**CustomTkinter**](https://github.com/TomSchimansky/CustomTkinter) - Modern Python GUI framework
- [**LangChain**](https://www.langchain.com/) - LLM application framework
- **Qwen 2.5 Coder** - Powerful coding models by Alibaba Cloud

---

##  Security

Please see [SECURITY.md](SECURITY.md) for our security policy and how to report vulnerabilities.

---

##  Support

-  **Documentation**: [SETUP_GUIDE.md](SETUP_GUIDE.md)
-  **Issues**: [GitHub Issues](https://github.com/yourusername/universal-knowledge-assistant/issues)
-  **Discussions**: [GitHub Discussions](https://github.com/yourusername/universal-knowledge-assistant/discussions)

---

<div align="center">

**Made with  for privacy-conscious knowledge workers**

 **Star this repo** if you find it useful!

</div>

## Features

- **Vector-based Semantic Search**: ChromaDB integration for fast, intelligent code retrieval
- **Split-Panel GUI**: Side-by-side display of user queries and assistant responses
- **Local First**: Runs entirely on your machine using Ollama (no cloud API required)
- **Context-Aware**: Upload specific files for targeted assistance
- **Model Flexibility**: Switch between different Qwen coder models
- **Dark Theme**: Clean, minimal interface inspired by modern development tools

## Prerequisites

1. **Python 3.8+** installed on your system
2. **Ollama** running locally with Qwen models:
   ```bash
   ollama pull qwen2.5-coder:7b
   ollama pull qwen2.5-coder:3b
   ollama pull qwen2.5-coder:1.5b
   ```
3. **Required Python packages** (see Installation)

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/Thurtea/llm-assistant.git
   cd llm-assistant
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create your configuration file:
   ```bash
   cp config.yaml.example config.yaml
   ```

4. Edit `config.yaml` and update the `codebase.path` to point to your project:
   ```yaml
   codebase:
     path: "/path/to/your/codebase"  # UPDATE THIS
   ```

## Usage

### GUI Mode (Recommended)

Launch the graphical interface:

```bash
python gui_assistant.py
```

**Windows Users**: Create a desktop shortcut for easy access:
```powershell
.\create_desktop_shortcut.ps1
```

### Python API Mode

Use the assistant programmatically:

```python
from assistant_core import LLMAssistant

# Initialize
assistant = LLMAssistant(
    model="qwen2.5-coder:7b",
    codebase_path="/path/to/your/code"
)

# Query with file context
response = assistant.query(
    "How does authentication work?",
    files=["auth/login.py", "auth/session.py"]
)
print(response)
```

### Vector Indexing (Recommended for Speed)

Create a vector database index for 10-100x faster queries:

```bash
python index_codebase.py
```

This creates a `chroma_db/` directory with semantic embeddings of your codebase. The GUI automatically uses the index when available.

**When to reindex:**
- After significant code changes
- When adding new files
- Run `python index_codebase.py` to rebuild

## GUI Features

- **Split Panel Layout**: User input on the left, assistant responses on the right
- **Copy Buttons**: One-click copy for either panel (clipboard icon)
- **Keyboard Shortcuts**: Ctrl+C (copy), Ctrl+A (select all), Ctrl+Enter (send)
- **Right-Click Menus**: Context menus with copy and select options
- **File Context**: Add specific files for targeted assistance
- **Model Switching**: Toggle between three models (7b/3b/1.5b) based on complexity
- **Status Feedback**: Real-time connection and processing status

## Configuration

Edit `config.yaml` to customize:

```yaml
models:
  default: "qwen2.5-coder:7b"      # Most capable, slower (~4GB RAM)
  balanced: "qwen2.5-coder:3b"     # Sweet spot for daily use (~2GB RAM)
  fast: "qwen2.5-coder:1.5b"       # Lightweight, quick responses (~1GB RAM)

codebase:
  path: "../your-project"         # Path to your code
  sync_on_start: true

context:
  max_lines_per_file: 300
  context_window: 16384

ollama:
  host: "http://localhost:11434"
  timeout: 60
```

## Requirements

See `requirements.txt` for full dependencies:
- `chromadb` - Vector database for semantic search
- `customtkinter` - Modern GUI framework
- `requests` - HTTP client for Ollama API
- `PyYAML` - Configuration file parsing
- `Pillow` - Image handling for GUI assets

## Project Structure

```
llm-assistant/
 assistant_core.py          # Core LLM logic
 indexed_assistant.py       # Vector search integration
 gui_assistant.py           # GUI application
 index_codebase.py          # Vector indexing script
 config.yaml.example        # Template configuration
 requirements.txt           # Python dependencies
 assets/                    # GUI assets (logos, icons)
 README.md
```

## License

MIT License - See LICENSE file for details

## Credits

Built with:
- [Ollama](https://ollama.ai/) - Local LLM inference
- [ChromaDB](https://www.trychroma.com/) - Vector database
- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) - Modern Tkinter
- Qwen 2.5 Coder models by Alibaba Cloud
