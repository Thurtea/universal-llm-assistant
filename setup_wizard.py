"""
Setup Wizard Backend Logic
Handles all backend operations for the first-run setup wizard.
"""

import os
import sys
import subprocess
import json
import yaml
import requests
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from PIL import Image


class SetupWizardBackend:
    """Backend logic for the setup wizard."""
    
    def __init__(self):
        self.script_dir = Path(__file__).parent
        self.config_path = self.script_dir / "config.yaml"
        self.setup_complete_marker = self.script_dir / ".setup_complete"
        self.ollama_host = "http://localhost:11434"
        
    def is_setup_complete(self) -> bool:
        """Check if setup has been completed before."""
        return self.setup_complete_marker.exists()
    
    def mark_setup_complete(self):
        """Create marker file indicating setup is complete."""
        self.setup_complete_marker.write_text(f"Setup completed at {Path.ctime(Path(__file__))}")
    
    # ========== DEPENDENCY CHECKS ==========
    
    def check_ollama_installed(self) -> Tuple[bool, str]:
        """
        Check if Ollama is installed and running.
        Returns: (is_installed, message)
        """
        try:
            response = requests.get(f"{self.ollama_host}/api/tags", timeout=3)
            if response.status_code == 200:
                return True, "Ollama is running"
            else:
                return False, f"Ollama responded with status {response.status_code}"
        except requests.exceptions.ConnectionError:
            return False, "Ollama is not running. Please start Ollama or install it from https://ollama.ai"
        except Exception as e:
            return False, f"Error checking Ollama: {str(e)}"
    
    def get_installed_models(self) -> List[str]:
        """
        Get list of installed Ollama models.
        Returns: List of model names
        """
        try:
            response = requests.get(f"{self.ollama_host}/api/tags", timeout=3)
            if response.status_code == 200:
                data = response.json()
                models = [model.get('name') for model in data.get('models', []) if model.get('name')]
                # Preserve order and remove duplicates
                return list(dict.fromkeys(models))
            return []
        except Exception:
            return []
    
    def check_python_packages(self) -> Tuple[bool, List[str]]:
        """
        Check if required Python packages are installed.
        Returns: (all_installed, missing_packages)
        """
        required_packages = [
            'ollama',
            'yaml',
            'customtkinter',
            'PIL',
            'chromadb',
            'sentence_transformers'
        ]
        
        missing = []
        for package in required_packages:
            try:
                if package == 'yaml':
                    __import__('yaml')
                elif package == 'PIL':
                    __import__('PIL')
                else:
                    __import__(package)
            except ImportError:
                missing.append(package)
        
        return len(missing) == 0, missing
    
    def install_python_packages(self, progress_callback=None) -> Tuple[bool, str]:
        """
        Install Python packages from requirements.txt.
        Returns: (success, message)
        """
        requirements_path = self.script_dir / "requirements.txt"
        if not requirements_path.exists():
            return False, "requirements.txt not found"
        
        try:
            if progress_callback:
                progress_callback("Installing Python dependencies...")
            
            # Use pip to install packages
            result = subprocess.run(
                [sys.executable, "-m", "pip", "install", "-r", str(requirements_path)],
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )
            
            if result.returncode == 0:
                return True, "Dependencies installed successfully"
            else:
                return False, f"pip install failed: {result.stderr}"
        except subprocess.TimeoutExpired:
            return False, "Installation timed out (5 minutes)"
        except Exception as e:
            return False, f"Error installing packages: {str(e)}"
    
    # ========== MODEL MANAGEMENT ==========
    
    def download_model(self, model_name: str, progress_callback=None) -> Tuple[bool, str]:
        """
        Download an Ollama model.
        Returns: (success, message)
        """
        try:
            if progress_callback:
                progress_callback(f"Downloading {model_name}... This may take several minutes.")
            
            # Start the pull
            response = requests.post(
                f"{self.ollama_host}/api/pull",
                json={"name": model_name},
                stream=True,
                timeout=1800  # 30 minute timeout for large models
            )
            
            if response.status_code == 200:
                # Stream the response to track progress
                for line in response.iter_lines():
                    if line:
                        try:
                            data = json.loads(line)
                            if progress_callback and 'status' in data:
                                progress_callback(f"{model_name}: {data['status']}")
                        except json.JSONDecodeError:
                            pass
                
                return True, f"Model {model_name} downloaded successfully"
            else:
                return False, f"Failed to download model: {response.text}"
        except Exception as e:
            return False, f"Error downloading model: {str(e)}"
    
    def get_recommended_model(self) -> str:
        """Get the recommended model name."""
        return "qwen2.5-coder:3b"

    def resolve_paths(self, models_location: Optional[str], database_location: Optional[str], install_dir: Optional[str]) -> Tuple[str, str, str]:
        """
        Normalize and fill defaults for paths. Expands env vars and resolves relative paths.
        Auto-detect common Ollama models path when `models_location` is None.
        """
        # Resolve models_location
        if models_location:
            ml = os.path.expandvars(models_location)
            ml = os.path.expanduser(ml)
        else:
            # Auto-detect default Ollama models path on Windows / Unix
            home = os.path.expanduser("~")
            default_win = os.path.join(os.environ.get("USERPROFILE", home), ".ollama", "models")
            default_unix = os.path.join(home, ".ollama", "models")
            ml = default_win if os.name == 'nt' else default_unix

        # Resolve database_location
        if database_location:
            db = os.path.expandvars(database_location)
            db = os.path.expanduser(db)
        else:
            db = os.path.join(os.getcwd(), "chroma_db")

        # Resolve install_dir
        if install_dir:
            inst = os.path.expandvars(install_dir)
            inst = os.path.expanduser(inst)
        else:
            inst = os.getcwd()

        # Make paths absolute
        ml = os.path.abspath(ml)
        db = os.path.abspath(db)
        inst = os.path.abspath(inst)
        return ml, db, inst
    
    # ========== CONFIGURATION ==========
    
    def create_config(
        self,
        app_name: str,
        selected_model: str,
        models_location: Optional[str] = None,
        database_location: Optional[str] = None,
        install_dir: Optional[str] = None,
        codebase_path: Optional[str] = None
    ) -> Tuple[bool, str]:
        """
        Create config.yaml from user inputs.
        Returns: (success, message)
        """
        try:
            # Resolve and normalize paths
            ml, db, inst = self.resolve_paths(models_location, database_location, install_dir)

            cfg = {
                'assistant': {
                    'name': app_name,
                    'version': '1.0.0'
                },
                'models': {
                    'default': selected_model,
                    'balanced': 'qwen2.5-coder:3b',
                    'fast': 'qwen2.5-coder:1.5b'
                },
                'paths': {
                    'models_location': ml,
                    'database_location': db,
                    'install_dir': inst
                },
                'codebase': {
                    'path': codebase_path or '../aethermud-code',
                    'sync_on_start': True
                },
                'context': {
                    'max_lines_per_file': 300,
                    'context_window': 16384
                },
                'ollama': {
                    'host': self.ollama_host,
                    'timeout': 60
                },
                'indexing': {
                    'collection_name': 'universal_knowledge',
                    'sync_on_start': True
                }
            }

            # Write YAML
            yaml_path = self.config_path
            with open(yaml_path, 'w', encoding='utf-8') as f:
                yaml.safe_dump(cfg, f, sort_keys=False)
            return True, f"Wrote config to {yaml_path}"
        except Exception as e:
            return False, f"Error creating config: {str(e)}"
    
    # ========== SHORTCUTS & FINALIZATION ==========
    
    def create_desktop_shortcut(self, app_name: str) -> Tuple[bool, str]:
        """
        Create a desktop shortcut using PowerShell.
        Returns: (success, message)
        """
        try:
            ps_script = self.script_dir / "create_desktop_shortcut.ps1"
            if not ps_script.exists():
                # Create a new shortcut script
                return self._create_shortcut_manual(app_name)
            
            # Run the existing PowerShell script
            result = subprocess.run(
                ["powershell", "-ExecutionPolicy", "Bypass", "-File", str(ps_script)],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                return True, "Desktop shortcut created"
            else:
                return False, f"Shortcut creation failed: {result.stderr}"
        except Exception as e:
            return False, f"Error creating shortcut: {str(e)}"
    
    def _create_shortcut_manual(self, app_name: str) -> Tuple[bool, str]:
        """Create desktop shortcut manually with PowerShell inline."""
        try:
            # Determine icon path - prefer existing favicon.ico
            icon_path = self.script_dir / "assets" / "universal-knowledge" / "favicon.ico"
            if not icon_path.exists():
                icon_path = self.script_dir / "assets" / "universal-knowledge" / "app.ico"
            if not icon_path.exists():
                icon_path = self.script_dir / "assets" / "favicon_io-AetherMUD" / "favicon.ico"
            
            # PowerShell script to create shortcut
            ps_script = f"""
$WshShell = New-Object -ComObject WScript.Shell
$DesktopPath = [Environment]::GetFolderPath("Desktop")
$ShortcutPath = Join-Path $DesktopPath "{app_name}.lnk"
$TargetPath = "pythonw.exe"
$Arguments = "`"{self.script_dir / 'launch_assistant_gui.pyw'}`""
$WorkingDir = "{self.script_dir}"
$IconPath = "{icon_path}"

if (Test-Path $ShortcutPath) {{
    Remove-Item $ShortcutPath -Force
}}

$Shortcut = $WshShell.CreateShortcut($ShortcutPath)
$Shortcut.TargetPath = $TargetPath
$Shortcut.Arguments = $Arguments
$Shortcut.WorkingDirectory = $WorkingDir
$Shortcut.IconLocation = $IconPath
$Shortcut.Description = "{app_name}"
$Shortcut.Save()

Write-Host "Shortcut created successfully"
"""
            
            result = subprocess.run(
                ["powershell", "-ExecutionPolicy", "Bypass", "-Command", ps_script],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                return True, "Desktop shortcut created"
            else:
                return False, f"Shortcut creation failed: {result.stderr}"
        except Exception as e:
            return False, f"Error creating shortcut: {str(e)}"
    
    def generate_icon_from_logo(self) -> Tuple[bool, str]:
        """
        Generate .ico file from logo PNG.
        Returns: (success, message)
        """
        try:
            # Check for existing favicon.ico first
            existing_ico = self.script_dir / "assets" / "universal-knowledge" / "favicon.ico"
            if existing_ico.exists():
                return True, f"Using existing icon: {existing_ico}"
            
            # Check for source logo
            logo_path = self.script_dir / "assets" / "universal-knowledge" / "LLM-Assistant-Logo.png"
            if not logo_path.exists():
                # Try alternative location
                logo_path = self.script_dir / "assets" / "favicon_io-AetherMUD" / "android-chrome-192x192.png"
                if not logo_path.exists():
                    return False, "No logo found to convert"
            
            # Output icon path
            icon_path = self.script_dir / "assets" / "universal-knowledge" / "app.ico"
            icon_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Open and resize logo
            img = Image.open(logo_path)
            
            # Convert to RGBA if needed
            if img.mode != 'RGBA':
                img = img.convert('RGBA')
            
            # Resize to 256x256
            img = img.resize((256, 256), Image.Resampling.LANCZOS)
            
            # Save as ICO with multiple sizes
            img.save(
                icon_path,
                format='ICO',
                sizes=[(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)]
            )
            
            return True, f"Icon generated at {icon_path}"
        except Exception as e:
            return False, f"Error generating icon: {str(e)}"
    
    def launch_main_app(self) -> Tuple[bool, str]:
        """
        Launch the main application (gui_assistant.py).
        Returns: (success, message)
        """
        try:
            app_path = self.script_dir / "gui_assistant.py"
            if not app_path.exists():
                return False, "Main application not found"
            
            # Launch in background without console window
            subprocess.Popen(
                [sys.executable, str(app_path)],
                creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == 'win32' else 0,
                cwd=self.script_dir
            )
            
            return True, "Application launched"
        except Exception as e:
            return False, f"Error launching app: {str(e)}"
    
    # ========== USE CASE DATA ==========
    
    def get_use_cases(self) -> List[Dict]:
        """Get list of use case examples."""
        return [
            {
                'title': 'Research Library',
                'description': 'Index academic papers, PDFs, and research notes',
                'icon': '📚',
                'recommended_model': 'qwen2.5-coder:7b',
                'example_path': 'E:\\Research-Papers'
            },
            {
                'title': 'Legal Documents',
                'description': 'Search contracts, case files, and legal briefs',
                'icon': '⚖️',
                'recommended_model': 'qwen2.5-coder:7b',
                'example_path': 'E:\\Legal-Files'
            },
            {
                'title': 'Medical Records',
                'description': 'Query patient notes locally (HIPAA-safe)',
                'icon': '🏥',
                'recommended_model': 'qwen2.5-coder:7b',
                'example_path': 'E:\\Medical-Records'
            },
            {
                'title': 'Code Development',
                'description': 'Index codebases, design docs, and APIs',
                'icon': '💻',
                'recommended_model': 'qwen2.5-coder:3b',
                'example_path': 'E:\\MyProject-Code'
            },
            {
                'title': 'Business Knowledge',
                'description': 'Search meeting notes, reports, and documents',
                'icon': '💼',
                'recommended_model': 'qwen2.5-coder:3b',
                'example_path': 'E:\\Business-Docs'
            },
            {
                'title': 'Personal Library',
                'description': 'Index books, articles, and personal notes',
                'icon': '📖',
                'recommended_model': 'qwen2.5-coder:3b',
                'example_path': 'E:\\My-Library'
            }
        ]
