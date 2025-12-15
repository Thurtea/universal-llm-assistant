# LLM Assistant

A local AI coding assistant powered by Ollama with vector-based semantic search and a clean dark-themed GUI. Built to provide intelligent codebase exploration with full context awareness.

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
- **Model Switching**: Toggle between default and fast models
- **Status Feedback**: Real-time connection and processing status

## Configuration

Edit `config.yaml` to customize:

```yaml
models:
  default: "qwen2.5-coder:7b"    # More capable, slower
  fast: "qwen2.5-coder:1.5b"     # Faster responses

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
├── assistant_core.py          # Core LLM logic
├── indexed_assistant.py       # Vector search integration
├── gui_assistant.py           # GUI application
├── index_codebase.py          # Vector indexing script
├── config.yaml.example        # Template configuration
├── requirements.txt           # Python dependencies
├── assets/                    # GUI assets (logos, icons)
└── README.md
```

## License

MIT License - See LICENSE file for details

## Credits

Built with:
- [Ollama](https://ollama.ai/) - Local LLM inference
- [ChromaDB](https://www.trychroma.com/) - Vector database
- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) - Modern Tkinter
- Qwen 2.5 Coder models by Alibaba Cloud
