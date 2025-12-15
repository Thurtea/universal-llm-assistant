"""
Universal Knowledge Assistant - First Run Setup Wizard
Professional GUI setup wizard for zero-terminal-knowledge setup.
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path
import threading
from typing import Optional
from setup_wizard import SetupWizardBackend

# ---- Professional Color Palette ----
BG_COLOR = "#0a0a0a"
PANEL_COLOR = "#111111"
INPUT_COLOR = "#151515"
BORDER_COLOR = "#262626"
TEXT_COLOR = "#f5f5f5"
MUTED_COLOR = "#9e9e9e"
ACCENT_COLOR = "#d4d4d4"
BUTTON_COLOR = "#1f1f1f"
BUTTON_HOVER = "#2a2a2a"
SUCCESS_COLOR = "#4ade80"
WARNING_COLOR = "#facc15"
ERROR_COLOR = "#f97373"

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class FirstRunSetupWizard(ctk.CTk):
    """First-run setup wizard with 5-screen progression."""
    
    def __init__(self):
        super().__init__()
        
        # Backend
        self.backend = SetupWizardBackend()
        
        # Window configuration
        self.title("Universal Knowledge Assistant - Setup Wizard")
        self.geometry("900x650")
        self.minsize(900, 650)
        self.configure(fg_color=BG_COLOR)
        
        # Try to set icon
        try:
            # Try universal-knowledge icon first
            icon_path = Path(__file__).parent / "assets" / "universal-knowledge" / "favicon.ico"
            if not icon_path.exists():
                icon_path = Path(__file__).parent / "assets" / "favicon_io-AetherMUD" / "favicon.ico"
            if icon_path.exists():
                self.iconbitmap(default=str(icon_path))
        except Exception:
            pass
        
        # State
        self.current_screen = 0
        self.screens = []
        self.config_data = {
            'app_name': 'Universal Knowledge Assistant',
            'knowledge_base_path': '',
            'selected_model': '',
            'create_shortcut': True,
            'launch_now': True
        }
        
        # Check if reconfigure mode
        self.reconfigure_mode = self.backend.is_setup_complete()
        
        # Build UI
        self._build_ui()
        self._show_screen(0)
    
    def _build_ui(self):
        """Build the main UI structure."""
        # Main container
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # Container frame
        self.container = ctk.CTkFrame(self, fg_color=BG_COLOR)
        self.container.grid(row=0, column=0, sticky="nsew", padx=40, pady=40)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        
        # Create all screens
        self.screens = [
            self._create_welcome_screen(),
            self._create_dependencies_screen(),
            self._create_configuration_screen(),
            self._create_use_cases_screen(),
            self._create_finalization_screen()
        ]
        
        # Stack all screens in the same position
        for screen in self.screens:
            screen.grid(row=0, column=0, sticky="nsew")
        
        # Navigation buttons
        self._create_navigation()
    
    # ========== SCREEN 1: WELCOME ==========
    
    def _create_welcome_screen(self):
        """Create the welcome screen."""
        frame = ctk.CTkFrame(self.container, fg_color=BG_COLOR)
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)
        
        content = ctk.CTkFrame(frame, fg_color=BG_COLOR)
        content.grid(row=0, column=0)
        
        # Logo (try to load)
        try:
            from PIL import Image
            # Try the new universal-knowledge logo first
            logo_path = Path(__file__).parent / "assets" / "universal-knowledge" / "LLM-Assistant-Logo.png"
            if not logo_path.exists():
                logo_path = Path(__file__).parent / "assets" / "universal-knowledge" / "android-chrome-192x192.png"
            if not logo_path.exists():
                logo_path = Path(__file__).parent / "assets" / "favicon_io-AetherMUD" / "android-chrome-192x192.png"
            
            if logo_path.exists():
                logo_pil = Image.open(logo_path)
                logo_ctk = ctk.CTkImage(
                    light_image=logo_pil,
                    dark_image=logo_pil,
                    size=(192, 192)
                )
                logo_label = ctk.CTkLabel(content, image=logo_ctk, text="")
                logo_label.image = logo_ctk
                logo_label.pack(pady=(0, 20))
        except Exception:
            pass
        
        # Title
        title = ctk.CTkLabel(
            content,
            text="Welcome to Universal Knowledge Assistant",
            font=("Inter", 28, "bold"),
            text_color=TEXT_COLOR
        )
        title.pack(pady=(0, 10))
        
        # Subtitle
        subtitle = ctk.CTkLabel(
            content,
            text="Index and query any knowledge base locally using AI",
            font=("Inter", 14),
            text_color=MUTED_COLOR
        )
        subtitle.pack(pady=(0, 30))
        
        # Features
        features_text = """
✓ Privacy-first: All processing happens locally
✓ AI-powered search: Natural language queries
✓ Multi-format support: PDF, code, text, and more
✓ Fast indexing: ChromaDB vector search
✓ Customizable: Choose your Ollama model

This wizard will help you set up everything in less than 2 minutes.
"""
        features = ctk.CTkLabel(
            content,
            text=features_text.strip(),
            font=("Inter", 12),
            text_color=TEXT_COLOR,
            justify="left"
        )
        features.pack(pady=(0, 20))
        
        # Reconfigure mode indicator
        if self.reconfigure_mode:
            reconfig_label = ctk.CTkLabel(
                content,
                text="⚙️ Reconfiguration Mode - Your previous setup will be updated",
                font=("Inter", 11),
                text_color=WARNING_COLOR
            )
            reconfig_label.pack(pady=(10, 0))
        
        return frame
    
    # ========== SCREEN 2: DEPENDENCIES ==========
    
    def _create_dependencies_screen(self):
        """Create the dependencies check screen."""
        frame = ctk.CTkFrame(self.container, fg_color=BG_COLOR)
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)
        
        content = ctk.CTkFrame(frame, fg_color=BG_COLOR)
        content.grid(row=0, column=0, sticky="nsew", padx=20)
        content.grid_columnconfigure(0, weight=1)
        
        # Title
        title = ctk.CTkLabel(
            content,
            text="Checking Dependencies",
            font=("Inter", 24, "bold"),
            text_color=TEXT_COLOR
        )
        title.grid(row=0, column=0, pady=(0, 30), sticky="w")
        
        # Ollama status
        self.ollama_status = ctk.CTkLabel(
            content,
            text="⏳ Checking Ollama...",
            font=("Inter", 12),
            text_color=MUTED_COLOR,
            anchor="w"
        )
        self.ollama_status.grid(row=1, column=0, pady=5, sticky="w")
        
        # Python packages status
        self.packages_status = ctk.CTkLabel(
            content,
            text="⏳ Checking Python packages...",
            font=("Inter", 12),
            text_color=MUTED_COLOR,
            anchor="w"
        )
        self.packages_status.grid(row=2, column=0, pady=5, sticky="w")
        
        # Install packages button (hidden by default)
        self.install_packages_btn = ctk.CTkButton(
            content,
            text="Install Missing Packages",
            command=self._install_packages,
            fg_color=BUTTON_COLOR,
            hover_color=BUTTON_HOVER,
            text_color=TEXT_COLOR,
            width=200
        )
        self.install_packages_btn.grid(row=3, column=0, pady=10, sticky="w")
        self.install_packages_btn.grid_remove()
        
        # Progress bar
        self.progress_bar = ctk.CTkProgressBar(
            content,
            mode="indeterminate",
            progress_color=SUCCESS_COLOR
        )
        self.progress_bar.grid(row=4, column=0, pady=10, sticky="ew")
        self.progress_bar.grid_remove()
        
        # Progress label
        self.progress_label = ctk.CTkLabel(
            content,
            text="",
            font=("Inter", 11),
            text_color=MUTED_COLOR,
            anchor="w"
        )
        self.progress_label.grid(row=5, column=0, pady=5, sticky="w")
        
        # Models section
        models_title = ctk.CTkLabel(
            content,
            text="Available Ollama Models",
            font=("Inter", 16, "bold"),
            text_color=TEXT_COLOR,
            anchor="w"
        )
        models_title.grid(row=6, column=0, pady=(20, 10), sticky="w")
        
        # Models list
        self.models_status = ctk.CTkLabel(
            content,
            text="⏳ Detecting models...",
            font=("Inter", 12),
            text_color=MUTED_COLOR,
            anchor="w"
        )
        self.models_status.grid(row=7, column=0, pady=5, sticky="w")
        
        # Download model button
        self.download_model_btn = ctk.CTkButton(
            content,
            text="Download Recommended Model (qwen2.5-coder:3b)",
            command=self._download_recommended_model,
            fg_color=BUTTON_COLOR,
            hover_color=BUTTON_HOVER,
            text_color=TEXT_COLOR,
            width=300
        )
        self.download_model_btn.grid(row=8, column=0, pady=10, sticky="w")
        self.download_model_btn.grid_remove()
        
        return frame
    
    # ========== SCREEN 3: CONFIGURATION ==========
    
    def _create_configuration_screen(self):
        """Create the configuration wizard screen."""
        frame = ctk.CTkFrame(self.container, fg_color=BG_COLOR)
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)
        
        content = ctk.CTkFrame(frame, fg_color=BG_COLOR)
        content.grid(row=0, column=0, sticky="nsew", padx=20)
        content.grid_columnconfigure(1, weight=1)
        
        # Title
        title = ctk.CTkLabel(
            content,
            text="Configuration",
            font=("Inter", 24, "bold"),
            text_color=TEXT_COLOR
        )
        title.grid(row=0, column=0, columnspan=2, pady=(0, 30), sticky="w")
        
        row = 1
        
        # Knowledge Base Path
        kb_label = ctk.CTkLabel(
            content,
            text="Knowledge Base Path:",
            font=("Inter", 12, "bold"),
            text_color=TEXT_COLOR,
            anchor="w"
        )
        kb_label.grid(row=row, column=0, pady=(10, 5), sticky="w")
        
        kb_help = ctk.CTkLabel(
            content,
            text="Select the folder containing files you want to search",
            font=("Inter", 10),
            text_color=MUTED_COLOR,
            anchor="w"
        )
        kb_help.grid(row=row+1, column=0, columnspan=2, pady=(0, 5), sticky="w")
        
        kb_frame = ctk.CTkFrame(content, fg_color=BG_COLOR)
        kb_frame.grid(row=row+2, column=0, columnspan=2, pady=(0, 20), sticky="ew")
        kb_frame.grid_columnconfigure(0, weight=1)
        
        self.kb_path_entry = ctk.CTkEntry(
            kb_frame,
            placeholder_text="E:\\My-Documents",
            fg_color=INPUT_COLOR,
            border_color=BORDER_COLOR,
            text_color=TEXT_COLOR
        )
        self.kb_path_entry.grid(row=0, column=0, sticky="ew", padx=(0, 10))
        
        kb_browse_btn = ctk.CTkButton(
            kb_frame,
            text="Browse...",
            command=self._browse_knowledge_base,
            fg_color=BUTTON_COLOR,
            hover_color=BUTTON_HOVER,
            text_color=TEXT_COLOR,
            width=100
        )
        kb_browse_btn.grid(row=0, column=1)
        
        row += 3
        
        # Model Selection
        model_label = ctk.CTkLabel(
            content,
            text="Model Selection:",
            font=("Inter", 12, "bold"),
            text_color=TEXT_COLOR,
            anchor="w"
        )
        model_label.grid(row=row, column=0, pady=(10, 5), sticky="w")
        
        model_help = ctk.CTkLabel(
            content,
            text="Choose which Ollama model to use for queries",
            font=("Inter", 10),
            text_color=MUTED_COLOR,
            anchor="w"
        )
        model_help.grid(row=row+1, column=0, columnspan=2, pady=(0, 5), sticky="w")
        
        self.model_var = ctk.StringVar(value="qwen2.5-coder:3b")
        self.model_dropdown = ctk.CTkOptionMenu(
            content,
            variable=self.model_var,
            values=["qwen2.5-coder:3b"],
            fg_color=BUTTON_COLOR,
            button_color=BUTTON_COLOR,
            button_hover_color=BUTTON_HOVER,
            text_color=TEXT_COLOR
        )
        self.model_dropdown.grid(row=row+2, column=0, columnspan=2, pady=(0, 20), sticky="ew")
        
        row += 3
        
        # Application Name
        app_name_label = ctk.CTkLabel(
            content,
            text="Application Name:",
            font=("Inter", 12, "bold"),
            text_color=TEXT_COLOR,
            anchor="w"
        )
        app_name_label.grid(row=row, column=0, pady=(10, 5), sticky="w")
        
        app_name_help = ctk.CTkLabel(
            content,
            text="Customize the window title and shortcut name",
            font=("Inter", 10),
            text_color=MUTED_COLOR,
            anchor="w"
        )
        app_name_help.grid(row=row+1, column=0, columnspan=2, pady=(0, 5), sticky="w")
        
        self.app_name_entry = ctk.CTkEntry(
            content,
            placeholder_text="Universal Knowledge Assistant",
            fg_color=INPUT_COLOR,
            border_color=BORDER_COLOR,
            text_color=TEXT_COLOR
        )
        self.app_name_entry.grid(row=row+2, column=0, columnspan=2, pady=(0, 20), sticky="ew")
        self.app_name_entry.insert(0, "Universal Knowledge Assistant")
        
        return frame
    
    # ========== SCREEN 4: USE CASES ==========
    
    def _create_use_cases_screen(self):
        """Create the use cases examples screen."""
        frame = ctk.CTkFrame(self.container, fg_color=BG_COLOR)
        frame.grid_rowconfigure(1, weight=1)
        frame.grid_columnconfigure(0, weight=1)
        
        # Title
        title = ctk.CTkLabel(
            frame,
            text="Use Case Examples",
            font=("Inter", 24, "bold"),
            text_color=TEXT_COLOR
        )
        title.grid(row=0, column=0, pady=(0, 20), sticky="w", padx=20)
        
        # Scrollable frame for use cases
        scroll_frame = ctk.CTkScrollableFrame(
            frame,
            fg_color=BG_COLOR,
            border_width=0
        )
        scroll_frame.grid(row=1, column=0, sticky="nsew", padx=20)
        scroll_frame.grid_columnconfigure(0, weight=1)
        scroll_frame.grid_columnconfigure(1, weight=1)
        
        # Get use cases from backend
        use_cases = self.backend.get_use_cases()
        
        # Create cards in 2-column grid
        for idx, use_case in enumerate(use_cases):
            row = idx // 2
            col = idx % 2
            
            card = self._create_use_case_card(scroll_frame, use_case)
            card.grid(row=row, column=col, padx=10, pady=10, sticky="ew")
        
        return frame
    
    def _create_use_case_card(self, parent, use_case):
        """Create a use case example card."""
        card = ctk.CTkFrame(
            parent,
            fg_color=PANEL_COLOR,
            border_color=BORDER_COLOR,
            border_width=1,
            corner_radius=6
        )
        
        # Icon and title
        header = ctk.CTkLabel(
            card,
            text=f"{use_case['icon']}  {use_case['title']}",
            font=("Inter", 14, "bold"),
            text_color=TEXT_COLOR,
            anchor="w"
        )
        header.pack(padx=15, pady=(15, 5), anchor="w")
        
        # Description
        desc = ctk.CTkLabel(
            card,
            text=use_case['description'],
            font=("Inter", 11),
            text_color=MUTED_COLOR,
            anchor="w",
            wraplength=300
        )
        desc.pack(padx=15, pady=(0, 10), anchor="w")
        
        # Recommended model badge
        badge = ctk.CTkLabel(
            card,
            text=f"Recommended: {use_case['recommended_model']}",
            font=("Inter", 9),
            text_color=ACCENT_COLOR,
            anchor="w"
        )
        badge.pack(padx=15, pady=(0, 15), anchor="w")
        
        return card
    
    # ========== SCREEN 5: FINALIZATION ==========
    
    def _create_finalization_screen(self):
        """Create the finalization screen."""
        frame = ctk.CTkFrame(self.container, fg_color=BG_COLOR)
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)
        
        content = ctk.CTkFrame(frame, fg_color=BG_COLOR)
        content.grid(row=0, column=0, sticky="nsew", padx=20)
        content.grid_columnconfigure(0, weight=1)
        
        # Title
        title = ctk.CTkLabel(
            content,
            text="Ready to Complete Setup",
            font=("Inter", 24, "bold"),
            text_color=TEXT_COLOR
        )
        title.grid(row=0, column=0, pady=(0, 20), sticky="w")
        
        # Summary section
        summary_title = ctk.CTkLabel(
            content,
            text="Configuration Summary:",
            font=("Inter", 14, "bold"),
            text_color=TEXT_COLOR,
            anchor="w"
        )
        summary_title.grid(row=1, column=0, pady=(10, 10), sticky="w")
        
        # Summary box
        self.summary_box = ctk.CTkTextbox(
            content,
            fg_color=PANEL_COLOR,
            text_color=TEXT_COLOR,
            border_color=BORDER_COLOR,
            border_width=1,
            height=200,
            font=("Consolas", 11)
        )
        self.summary_box.grid(row=2, column=0, pady=(0, 20), sticky="ew")
        
        # Options
        options_title = ctk.CTkLabel(
            content,
            text="Options:",
            font=("Inter", 14, "bold"),
            text_color=TEXT_COLOR,
            anchor="w"
        )
        options_title.grid(row=3, column=0, pady=(10, 10), sticky="w")
        
        # Create desktop shortcut checkbox
        self.shortcut_var = ctk.BooleanVar(value=True)
        shortcut_cb = ctk.CTkCheckBox(
            content,
            text="Create desktop shortcut",
            variable=self.shortcut_var,
            fg_color=BUTTON_COLOR,
            hover_color=BUTTON_HOVER,
            text_color=TEXT_COLOR
        )
        shortcut_cb.grid(row=4, column=0, pady=5, sticky="w")
        
        # Launch assistant now checkbox
        self.launch_var = ctk.BooleanVar(value=True)
        launch_cb = ctk.CTkCheckBox(
            content,
            text="Launch assistant now",
            variable=self.launch_var,
            fg_color=BUTTON_COLOR,
            hover_color=BUTTON_HOVER,
            text_color=TEXT_COLOR
        )
        launch_cb.grid(row=5, column=0, pady=5, sticky="w")
        
        # Finish button
        self.finish_btn = ctk.CTkButton(
            content,
            text="🚀 Finish Setup",
            command=self._finish_setup,
            fg_color=SUCCESS_COLOR,
            hover_color="#3cbd6f",
            text_color="#000000",
            font=("Inter", 14, "bold"),
            height=40
        )
        self.finish_btn.grid(row=6, column=0, pady=(30, 10), sticky="ew")
        
        # Status label
        self.final_status = ctk.CTkLabel(
            content,
            text="",
            font=("Inter", 11),
            text_color=MUTED_COLOR,
            anchor="w"
        )
        self.final_status.grid(row=7, column=0, pady=5, sticky="w")
        
        return frame
    
    # ========== NAVIGATION ==========
    
    def _create_navigation(self):
        """Create navigation buttons."""
        nav_frame = ctk.CTkFrame(self.container, fg_color=BG_COLOR)
        nav_frame.grid(row=1, column=0, sticky="ew", pady=(20, 0))
        nav_frame.grid_columnconfigure(0, weight=1)
        
        # Progress indicator
        self.progress_text = ctk.CTkLabel(
            nav_frame,
            text="Step 1 of 5",
            font=("Inter", 11),
            text_color=MUTED_COLOR
        )
        self.progress_text.grid(row=0, column=0, sticky="w")
        
        # Buttons
        btn_frame = ctk.CTkFrame(nav_frame, fg_color=BG_COLOR)
        btn_frame.grid(row=0, column=1, sticky="e")
        
        self.back_btn = ctk.CTkButton(
            btn_frame,
            text="← Back",
            command=self._go_back,
            fg_color=BUTTON_COLOR,
            hover_color=BUTTON_HOVER,
            text_color=TEXT_COLOR,
            width=100
        )
        self.back_btn.grid(row=0, column=0, padx=(0, 10))
        
        self.next_btn = ctk.CTkButton(
            btn_frame,
            text="Next →",
            command=self._go_next,
            fg_color=BUTTON_COLOR,
            hover_color=BUTTON_HOVER,
            text_color=TEXT_COLOR,
            width=100
        )
        self.next_btn.grid(row=0, column=1)
    
    def _show_screen(self, index):
        """Show a specific screen."""
        self.current_screen = index
        
        # Hide all screens
        for screen in self.screens:
            screen.grid_remove()
        
        # Show current screen
        self.screens[index].grid()
        
        # Update progress
        self.progress_text.configure(text=f"Step {index + 1} of 5")
        
        # Update navigation buttons
        self.back_btn.configure(state="normal" if index > 0 else "disabled")
        
        # Hide next button on finalization screen
        if index == 4:
            self.next_btn.grid_remove()
        else:
            self.next_btn.grid()
            self.next_btn.configure(state="normal")
        
        # Run screen-specific initialization
        if index == 1:
            self._check_dependencies()
        elif index == 2:
            self._populate_configuration()
        elif index == 4:
            self._populate_summary()
    
    def _go_back(self):
        """Go to previous screen."""
        if self.current_screen > 0:
            self._show_screen(self.current_screen - 1)
    
    def _go_next(self):
        """Go to next screen."""
        # Validate current screen before proceeding
        if self.current_screen == 2:
            if not self._validate_configuration():
                return
        
        if self.current_screen < len(self.screens) - 1:
            self._show_screen(self.current_screen + 1)
    
    # ========== SCREEN-SPECIFIC LOGIC ==========
    
    def _check_dependencies(self):
        """Check dependencies on screen 2."""
        threading.Thread(target=self._check_dependencies_thread, daemon=True).start()
    
    def _check_dependencies_thread(self):
        """Background thread to check dependencies."""
        # Check Ollama
        self.after(0, lambda: self.ollama_status.configure(text="⏳ Checking Ollama..."))
        ollama_ok, ollama_msg = self.backend.check_ollama_installed()
        
        if ollama_ok:
            self.after(0, lambda: self.ollama_status.configure(
                text=f"✅ {ollama_msg}",
                text_color=SUCCESS_COLOR
            ))
        else:
            self.after(0, lambda: self.ollama_status.configure(
                text=f"❌ {ollama_msg}",
                text_color=ERROR_COLOR
            ))
        
        # Check Python packages
        self.after(0, lambda: self.packages_status.configure(text="⏳ Checking Python packages..."))
        packages_ok, missing = self.backend.check_python_packages()
        
        if packages_ok:
            self.after(0, lambda: self.packages_status.configure(
                text="✅ All Python packages installed",
                text_color=SUCCESS_COLOR
            ))
        else:
            missing_str = ", ".join(missing)
            self.after(0, lambda: self.packages_status.configure(
                text=f"❌ Missing packages: {missing_str}",
                text_color=ERROR_COLOR
            ))
            self.after(0, lambda: self.install_packages_btn.grid())
        
        # Check models
        self.after(0, lambda: self.models_status.configure(text="⏳ Detecting Ollama models..."))
        if ollama_ok:
            models = self.backend.get_installed_models()
            
            if models:
                models_str = ", ".join(models)
                self.after(0, lambda: self.models_status.configure(
                    text=f"✅ Found models: {models_str}",
                    text_color=SUCCESS_COLOR
                ))
                # Store models for configuration screen
                self.available_models = models
            else:
                self.after(0, lambda: self.models_status.configure(
                    text="⚠️ No models detected",
                    text_color=WARNING_COLOR
                ))
                self.after(0, lambda: self.download_model_btn.grid())
                self.available_models = []
        else:
            self.after(0, lambda: self.models_status.configure(
                text="⚠️ Cannot detect models (Ollama not running)",
                text_color=WARNING_COLOR
            ))
            self.available_models = []
    
    def _install_packages(self):
        """Install Python packages."""
        self.install_packages_btn.configure(state="disabled")
        self.progress_bar.grid()
        self.progress_bar.start()
        
        threading.Thread(target=self._install_packages_thread, daemon=True).start()
    
    def _install_packages_thread(self):
        """Background thread to install packages."""
        def progress_callback(msg):
            self.after(0, lambda: self.progress_label.configure(text=msg))
        
        success, message = self.backend.install_python_packages(progress_callback)
        
        self.after(0, lambda: self.progress_bar.stop())
        self.after(0, lambda: self.progress_bar.grid_remove())
        
        if success:
            self.after(0, lambda: self.packages_status.configure(
                text=f"✅ {message}",
                text_color=SUCCESS_COLOR
            ))
            self.after(0, lambda: self.install_packages_btn.grid_remove())
            self.after(0, lambda: self.progress_label.configure(text=""))
        else:
            self.after(0, lambda: self.progress_label.configure(
                text=f"❌ {message}",
                text_color=ERROR_COLOR
            ))
            self.after(0, lambda: self.install_packages_btn.configure(state="normal"))
    
    def _download_recommended_model(self):
        """Download the recommended model."""
        self.download_model_btn.configure(state="disabled")
        self.progress_bar.grid()
        self.progress_bar.start()
        
        threading.Thread(target=self._download_model_thread, daemon=True).start()
    
    def _download_model_thread(self):
        """Background thread to download model."""
        model_name = self.backend.get_recommended_model()
        
        def progress_callback(msg):
            self.after(0, lambda: self.progress_label.configure(text=msg))
        
        success, message = self.backend.download_model(model_name, progress_callback)
        
        self.after(0, lambda: self.progress_bar.stop())
        self.after(0, lambda: self.progress_bar.grid_remove())
        
        if success:
            self.after(0, lambda: self.models_status.configure(
                text=f"✅ {message}",
                text_color=SUCCESS_COLOR
            ))
            self.after(0, lambda: self.download_model_btn.grid_remove())
            self.after(0, lambda: self.progress_label.configure(text=""))
            # Add to available models
            if not hasattr(self, 'available_models'):
                self.available_models = []
            self.available_models.append(model_name)
        else:
            self.after(0, lambda: self.progress_label.configure(
                text=f"❌ {message}",
                text_color=ERROR_COLOR
            ))
            self.after(0, lambda: self.download_model_btn.configure(state="normal"))
    
    def _browse_knowledge_base(self):
        """Browse for knowledge base folder."""
        folder = filedialog.askdirectory(
            title="Select Knowledge Base Folder",
            initialdir=str(Path.home())
        )
        if folder:
            self.kb_path_entry.delete(0, 'end')
            self.kb_path_entry.insert(0, folder)
    
    def _populate_configuration(self):
        """Populate configuration screen with available models."""
        if hasattr(self, 'available_models') and self.available_models:
            self.model_dropdown.configure(values=self.available_models)
            self.model_var.set(self.available_models[0])
        else:
            self.model_dropdown.configure(values=["qwen2.5-coder:3b"])
            self.model_var.set("qwen2.5-coder:3b")
    
    def _validate_configuration(self):
        """Validate configuration inputs."""
        kb_path = self.kb_path_entry.get().strip()
        app_name = self.app_name_entry.get().strip()
        
        if not kb_path:
            messagebox.showerror("Validation Error", "Please select a knowledge base path")
            return False
        
        if not Path(kb_path).exists():
            messagebox.showerror("Validation Error", "The selected knowledge base path does not exist")
            return False
        
        if not app_name:
            messagebox.showerror("Validation Error", "Please enter an application name")
            return False
        
        # Save configuration
        self.config_data['knowledge_base_path'] = kb_path
        self.config_data['app_name'] = app_name
        self.config_data['selected_model'] = self.model_var.get()
        
        return True
    
    def _populate_summary(self):
        """Populate the summary box."""
        summary = f"""Application Name: {self.config_data['app_name']}
Knowledge Base: {self.config_data['knowledge_base_path']}
Selected Model: {self.config_data['selected_model']}

Setup will:
• Create config.yaml with your settings
• Generate application icon
• Configure the knowledge assistant
"""
        
        if self.shortcut_var.get():
            summary += "• Create desktop shortcut\n"
        
        if self.launch_var.get():
            summary += "• Launch the assistant\n"
        
        self.summary_box.configure(state="normal")
        self.summary_box.delete("1.0", "end")
        self.summary_box.insert("1.0", summary)
        self.summary_box.configure(state="disabled")
    
    def _finish_setup(self):
        """Finalize the setup."""
        self.finish_btn.configure(state="disabled", text="Setting up...")
        self.final_status.configure(text="Creating configuration...", text_color=MUTED_COLOR)
        
        threading.Thread(target=self._finish_setup_thread, daemon=True).start()
    
    def _finish_setup_thread(self):
        """Background thread to finish setup."""
        # Step 1: Create config
        success, message = self.backend.create_config(
            self.config_data['app_name'],
            self.config_data['knowledge_base_path'],
            self.config_data['selected_model']
        )
        
        if not success:
            self.after(0, lambda: self.final_status.configure(
                text=f"❌ {message}",
                text_color=ERROR_COLOR
            ))
            self.after(0, lambda: self.finish_btn.configure(state="normal", text="🚀 Finish Setup"))
            return
        
        self.after(0, lambda: self.final_status.configure(
            text="✅ Configuration created",
            text_color=SUCCESS_COLOR
        ))
        
        # Step 2: Generate icon
        self.after(0, lambda: self.final_status.configure(
            text="Generating application icon...",
            text_color=MUTED_COLOR
        ))
        
        icon_success, icon_msg = self.backend.generate_icon_from_logo()
        # Icon generation is optional, continue even if it fails
        
        # Step 3: Create shortcut if requested
        if self.shortcut_var.get():
            self.after(0, lambda: self.final_status.configure(
                text="Creating desktop shortcut...",
                text_color=MUTED_COLOR
            ))
            
            shortcut_success, shortcut_msg = self.backend.create_desktop_shortcut(
                self.config_data['app_name']
            )
            
            if shortcut_success:
                self.after(0, lambda: self.final_status.configure(
                    text="✅ Desktop shortcut created",
                    text_color=SUCCESS_COLOR
                ))
        
        # Step 4: Mark setup complete
        self.backend.mark_setup_complete()
        
        # Step 5: Launch if requested
        if self.launch_var.get():
            self.after(0, lambda: self.final_status.configure(
                text="Launching assistant...",
                text_color=MUTED_COLOR
            ))
            
            launch_success, launch_msg = self.backend.launch_main_app()
        
        # Final message
        self.after(0, lambda: self.final_status.configure(
            text="✅ Setup complete!",
            text_color=SUCCESS_COLOR
        ))
        
        # Close wizard after a delay
        self.after(2000, self.destroy)


def main():
    """Main entry point."""
    app = FirstRunSetupWizard()
    app.mainloop()


if __name__ == "__main__":
    main()
