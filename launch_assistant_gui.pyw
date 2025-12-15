"""
Thurtea Assistant - GUI Launcher
Launches the assistant without showing a terminal window
"""

import sys
from pathlib import Path

# Set working directory to llm-assistant folder
script_dir = Path(__file__).parent
sys.path.insert(0, str(script_dir))

# Launch GUI
from gui_assistant import main

if __name__ == "__main__":
    main()
