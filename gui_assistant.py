"""
Thurtea · AetherMUD LLM Assistant
GUI wrapper around LLMAssistant with Thurtea.com-inspired dark minimal design.
"""

import customtkinter as ctk
import tkinter as tk
from pathlib import Path
import threading
import yaml
from PIL import Image, ImageTk
from assistant_core import LLMAssistant

# ---- Thurtea Brand Palette ----
THURTEA_BG = "#0a0a0a"          # Overall background
THURTEA_PANEL = "#111111"       # Panels / cards
THURTEA_INPUT = "#151515"       # Input fields
THURTEA_BORDER = "#262626"      # Subtle borders
THURTEA_TEXT = "#f5f5f5"        # Primary text
THURTEA_MUTED = "#9e9e9e"       # Secondary text
THURTEA_ACCENT = "#d4d4d4"      # Light accent (lines, subtle highlights)
THURTEA_BUTTON = "#1f1f1f"      # Buttons
THURTEA_BUTTON_HOVER = "#2a2a2a"

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")  # We override with custom colors


class ThurteaAssistantApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Load config
        with open("config.yaml", "r", encoding="utf-8") as f:
            self.config = yaml.safe_load(f)

        # Core assistant selection (indexed preferred if available)
        index_path = Path("./chroma_db")
        self.indexed_mode = False
        if index_path.exists():
            try:
                from indexed_assistant import IndexedAssistant

                self.assistant = IndexedAssistant(
                    model=self.config["models"]["default"],
                    index_path=str(index_path),
                )
                self.indexed_mode = True
                print("✅ Using indexed search (fast mode)")
            except Exception as e:
                print(f"⚠️ Indexed load failed, falling back: {e}")
                self.assistant = LLMAssistant(
                    model=self.config["models"]["default"],
                    codebase_path=self.config["codebase"]["path"],
                    context_window=self.config["context"]["context_window"],
                )
        else:
            self.assistant = LLMAssistant(
                model=self.config["models"]["default"],
                codebase_path=self.config["codebase"]["path"],
                context_window=self.config["context"]["context_window"],
            )
            print("⚠️ Using direct file access (run index_codebase.py for speed)")

        import yaml
        from pathlib import Path

        config_path = Path(__file__).parent / "config.yaml"
        with open(config_path, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)

        # Window configuration
        self.title(config.get("assistant", {}).get("name", "Universal Knowledge Assistant"))
        self.geometry("1100x700")
        self.minsize(900, 600)
        self.configure(fg_color=THURTEA_BG)

        self._status_flash_token = None

        # Window icon (favicon)
        try:
            script_dir = Path(__file__).parent
            icon_path = script_dir / "assets" / "favicon_io-AetherMUD" / "favicon.ico"
            if icon_path.exists():
                self.iconbitmap(default=str(icon_path))
        except Exception:
            pass

        # State
        self.selected_files = []  # relative paths from ../aethermud-code

        # Layout
        self._build_layout()

    # ---------- Layout ----------

    def _build_layout(self):
        # Use a vertical layout: header, nav, body, input
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self._build_header()
        self._build_navbar()
        self._build_body()
        self._build_input_area()

    def _build_header(self):
        header = ctk.CTkFrame(self, fg_color=THURTEA_BG)
        header.grid(row=0, column=0, sticky="ew", padx=0, pady=(20, 10))
        header.grid_columnconfigure(0, weight=1)

        # Load and display logo
        try:
            script_dir = Path(__file__).parent
            logo_path = script_dir / "assets" / "favicon_io-AetherMUD" / "android-chrome-192x192.png"
            if logo_path.exists():
                logo_pil = Image.open(logo_path)
                logo_ctk = ctk.CTkImage(
                    light_image=logo_pil,
                    dark_image=logo_pil,
                    size=(192, 192)
                )

                logo_label = ctk.CTkLabel(
                    header,
                    image=logo_ctk,
                    text=""
                )
                logo_label.image = logo_ctk
                logo_label.grid(row=0, column=0, sticky="n", pady=(0, 5))
        except Exception as e:
            # Fallback to text if logo fails
            pass

        subtitle = ctk.CTkLabel(
            header,
            text="AetherMUD Assistant",
            font=("Inter", 13),
            text_color=THURTEA_MUTED,
        )
        subtitle.grid(row=1, column=0, sticky="n")

    def _build_navbar(self):
        nav = ctk.CTkFrame(self, fg_color=THURTEA_BG)
        nav.grid(row=1, column=0, sticky="ew", padx=40, pady=(10, 10))
        nav.grid_columnconfigure(0, weight=1)
        nav.grid_columnconfigure(1, weight=0)
        nav.grid_columnconfigure(2, weight=0)

        # Left: thin accent line (visual separator, like your site)
        line = ctk.CTkLabel(
            nav, text="", fg_color=THURTEA_ACCENT, height=1
        )
        line.grid(row=0, column=0, sticky="ew", pady=(10, 10), padx=(0, 20))

        # Model selector
        self.model_var = ctk.StringVar(value=self.config["models"]["default"])
        model_menu = ctk.CTkOptionMenu(
            nav,
            values=[
                self.config["models"]["default"],
                self.config["models"].get("balanced", "qwen2.5-coder:3b"),
                self.config["models"]["fast"],
            ],
            variable=self.model_var,
            command=self._on_model_change,
            fg_color=THURTEA_BUTTON,
            button_color=THURTEA_BUTTON,
            button_hover_color=THURTEA_BUTTON_HOVER,
            text_color=THURTEA_TEXT,
        )
        model_menu.grid(row=0, column=1, padx=(0, 10), sticky="e")

        # Status
        self.status_label = ctk.CTkLabel(
            nav,
            text=self._ready_status_text(),
            font=("Inter", 11),
            text_color=THURTEA_MUTED,
        )
        self.status_label.grid(row=0, column=2, sticky="e")

    def _build_body(self):
        body = ctk.CTkFrame(self, fg_color=THURTEA_BG)
        body.grid(row=2, column=0, sticky="nsew", padx=40, pady=(0, 10))
        body.grid_rowconfigure(0, weight=1)
        body.grid_columnconfigure(0, weight=1)
        body.grid_columnconfigure(1, weight=1)

        # Left Panel: User Input
        left_panel = ctk.CTkFrame(
            body,
            fg_color=THURTEA_PANEL,
            border_color=THURTEA_BORDER,
            border_width=1,
            corner_radius=6,
        )
        left_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 5))
        left_panel.grid_rowconfigure(1, weight=1)
        left_panel.grid_columnconfigure(0, weight=1)

        # Left panel header with copy button
        left_header = ctk.CTkFrame(left_panel, fg_color=THURTEA_PANEL)
        left_header.grid(row=0, column=0, sticky="ew", padx=12, pady=(12, 6))
        left_header.grid_columnconfigure(0, weight=1)

        left_title = ctk.CTkLabel(
            left_header,
            text="Your Input",
            font=("Inter", 12, "bold"),
            text_color=THURTEA_ACCENT,
        )
        left_title.grid(row=0, column=0, sticky="w")

        self.copy_user_btn = ctk.CTkButton(
            left_header,
            text="📋",
            width=32,
            height=24,
            command=lambda: self._copy_panel_text(self.user_box),
            fg_color=THURTEA_BUTTON,
            hover_color=THURTEA_BUTTON_HOVER,
            text_color=THURTEA_TEXT,
        )
        self.copy_user_btn.grid(row=0, column=1, sticky="e")

        # User text box
        self.user_box = ctk.CTkTextbox(
            left_panel,
            fg_color=THURTEA_PANEL,
            text_color=THURTEA_TEXT,
            border_width=0,
            font=("Consolas", 11),
            wrap="word",
        )
        self.user_box.grid(row=1, column=0, sticky="nsew", padx=12, pady=(0, 12))
        self.user_box.configure(state="disabled")

        # Right Panel: Assistant Response
        right_panel = ctk.CTkFrame(
            body,
            fg_color=THURTEA_PANEL,
            border_color=THURTEA_BORDER,
            border_width=1,
            corner_radius=6,
        )
        right_panel.grid(row=0, column=1, sticky="nsew", padx=(5, 0))
        right_panel.grid_rowconfigure(1, weight=1)
        right_panel.grid_columnconfigure(0, weight=1)

        # Right panel header with copy button
        right_header = ctk.CTkFrame(right_panel, fg_color=THURTEA_PANEL)
        right_header.grid(row=0, column=0, sticky="ew", padx=12, pady=(12, 6))
        right_header.grid_columnconfigure(0, weight=1)

        right_title = ctk.CTkLabel(
            right_header,
            text="Assistant Response",
            font=("Inter", 12, "bold"),
            text_color=THURTEA_ACCENT,
        )
        right_title.grid(row=0, column=0, sticky="w")

        self.copy_assistant_btn = ctk.CTkButton(
            right_header,
            text="📋",
            width=32,
            height=24,
            command=lambda: self._copy_panel_text(self.assistant_box),
            fg_color=THURTEA_BUTTON,
            hover_color=THURTEA_BUTTON_HOVER,
            text_color=THURTEA_TEXT,
        )
        self.copy_assistant_btn.grid(row=0, column=1, sticky="e")

        # Assistant text box
        self.assistant_box = ctk.CTkTextbox(
            right_panel,
            fg_color=THURTEA_PANEL,
            text_color=THURTEA_TEXT,
            border_width=0,
            font=("Consolas", 11),
            wrap="word",
        )
        self.assistant_box.grid(row=1, column=0, sticky="nsew", padx=12, pady=(0, 12))
        self.assistant_box.configure(state="disabled")

        # Initialize interactions for both text boxes
        self._init_text_box_interactions(self.user_box)
        self._init_text_box_interactions(self.assistant_box)

        # Welcome text in the assistant panel
        self._append_to_box(
            self.assistant_box,
            "Thurtea · AetherMUD Assistant ready.\n"
            "Ask questions about your codebase, or add file context.",
            THURTEA_MUTED
        )

    def _build_input_area(self):
        input_frame = ctk.CTkFrame(self, fg_color=THURTEA_BG)
        input_frame.grid(row=3, column=0, sticky="ew", padx=40, pady=(0, 20))
        input_frame.grid_columnconfigure(0, weight=1)
        input_frame.grid_columnconfigure(1, weight=0)
        input_frame.grid_rowconfigure(0, weight=1)
        input_frame.grid_rowconfigure(1, weight=0)

        # Multi-line input
        self.input_box = ctk.CTkTextbox(
            input_frame,
            fg_color=THURTEA_INPUT,
            text_color=THURTEA_TEXT,
            border_color=THURTEA_BORDER,
            border_width=1,
            height=80,
            font=("Consolas", 11),
            wrap="word",
        )
        self.input_box.grid(
            row=0, column=0, columnspan=2, sticky="ew", padx=(0, 10), pady=(0, 8)
        )
        self.input_box.bind("<Control-Return>", self._on_send_shortcut)

        # Left bottom: context label
        self.context_label = ctk.CTkLabel(
            input_frame,
            text="Context: none",
            font=("Inter", 10),
            text_color=THURTEA_MUTED,
        )
        self.context_label.grid(row=1, column=0, sticky="w")

        # Right bottom: buttons (stacked visually)
        buttons_frame = ctk.CTkFrame(input_frame, fg_color=THURTEA_BG)
        buttons_frame.grid(row=1, column=1, sticky="e")

        self.context_button = ctk.CTkButton(
            buttons_frame,
            text="Add File Context",
            command=self._on_add_context,
            fg_color=THURTEA_BUTTON,
            hover_color=THURTEA_BUTTON_HOVER,
            text_color=THURTEA_TEXT,
            width=150,
        )
        self.context_button.grid(row=0, column=0, padx=(0, 8))

        self.send_button = ctk.CTkButton(
            buttons_frame,
            text="Send (Ctrl+Enter)",
            command=self._on_send_clicked,
            fg_color=THURTEA_BUTTON,
            hover_color=THURTEA_BUTTON_HOVER,
            text_color=THURTEA_TEXT,
            width=150,
        )
        self.send_button.grid(row=0, column=1)

    # ---------- Helpers ----------

    def _set_status(self, text: str, level: str = "info"):
        self._status_flash_token = None
        color_map = {
            "info": THURTEA_MUTED,
            "ok": "#4ade80",       # green-ish
            "warn": "#facc15",     # yellow-ish
            "error": "#f97373",    # red-ish
        }
        self.status_label.configure(text=text, text_color=color_map.get(level, THURTEA_MUTED))

    def _ready_status_text(self) -> str:
        text = "Ready · Ollama: Connected"
        if getattr(self, "indexed_mode", False):
            text += " · Indexed ⚡"
        return text

    def _append_to_box(self, textbox: ctk.CTkTextbox, content: str, text_color: str):
        """Append text to a specific textbox."""
        textbox.configure(state="normal")
        textbox.insert("end", content + "\n\n")
        textbox.configure(state="disabled")
        textbox.see("end")

    def _append_user(self, message: str):
        self._append_to_box(self.user_box, message, THURTEA_TEXT)

    def _append_assistant(self, message: str):
        self._append_to_box(self.assistant_box, message, THURTEA_TEXT)

    def _flash_status(self, text: str, level: str = "info", duration_ms: int = 1200):
        previous_text = self.status_label.cget("text")
        previous_color = self.status_label.cget("text_color")
        self._set_status(text, level)
        token = object()
        self._status_flash_token = token
        self.after(duration_ms, lambda: self._restore_status(token, previous_text, previous_color))

    def _restore_status(self, token, previous_text, previous_color):
        if getattr(self, "_status_flash_token", None) is token:
            self._status_flash_token = None
            self.status_label.configure(text=previous_text, text_color=previous_color)

    def _init_text_box_interactions(self, textbox: ctk.CTkTextbox):
        """Initialize interactions for a textbox (selection, copy, context menu)."""
        # Configure selection visuals using the underlying text widget
        text_widget = textbox._textbox
        text_widget.configure(
            selectbackground="#2d2d2d",
            selectforeground=THURTEA_TEXT,
            insertbackground=THURTEA_TEXT,
            cursor="xterm",
        )

        textbox.bind("<Button-1>", lambda e: textbox.focus_set())
        textbox.bind("<Control-a>", lambda e: self._on_select_all(e, textbox))
        textbox.bind("<Control-A>", lambda e: self._on_select_all(e, textbox))
        textbox.bind("<Control-c>", lambda e: self._on_copy(e, textbox))
        textbox.bind("<Control-C>", lambda e: self._on_copy(e, textbox))
        textbox.bind("<Button-3>", lambda e: self._show_context_menu(e, textbox))

        # Create context menu for this textbox
        context_menu = tk.Menu(
            textbox,
            tearoff=0,
            bg=THURTEA_PANEL,
            fg=THURTEA_TEXT,
            activebackground=THURTEA_BUTTON_HOVER,
            activeforeground=THURTEA_TEXT,
            borderwidth=0,
        )
        context_menu.add_command(
            label="Copy", 
            command=lambda: self._copy_selected_from_box(textbox)
        )
        context_menu.add_command(
            label="Select All", 
            command=lambda: self._select_all_in_box(textbox)
        )
        # Store context menu reference
        textbox._context_menu = context_menu

    # ---------- Events ----------

    def _on_model_change(self, model_name: str):
        self.assistant.model = model_name
        self._set_status(f"Model set to {model_name}", "info")

    def _on_send_shortcut(self, event):
        self._on_send_clicked()
        return "break"

    def _on_send_clicked(self):
        query = self.input_box.get("1.0", "end-1c").strip()
        if not query:
            return

        self.input_box.delete("1.0", "end")
        self._append_user(query)
        self._set_status("Thinking...", "warn")
        self.send_button.configure(state="disabled", text="Thinking…")

        # Run in background
        threading.Thread(target=self._run_query, args=(query,), daemon=True).start()

    def _run_query(self, query: str):
        try:
            files = self.selected_files if self.selected_files else None
            response = self.assistant.query(query, files=files)
            self.after(0, lambda: self._append_assistant(response))
            self.after(0, lambda: self._set_status(self._ready_status_text(), "ok"))
        except Exception as e:
            self.after(0, lambda: self._append_system(f"Error: {e}"))
            self.after(0, lambda: self._set_status("Error talking to model", "error"))
        finally:
            self.after(0, lambda: self.send_button.configure(state="normal", text="Send (Ctrl+Enter)"))

    def _on_add_context(self):
        from tkinter import filedialog

        codebase_root = Path(self.config["codebase"]["path"]).resolve()
        initial_dir = codebase_root

        file_paths = filedialog.askopenfilenames(
            title="Select AetherMUD files for context",
            initialdir=initial_dir,
            filetypes=[("Python files", "*.py"), ("All files", "*.*")],
        )
        if not file_paths:
            return

        rel_paths = []
        for f in file_paths:
            p = Path(f).resolve()
            try:
                rel = p.relative_to(codebase_root)
                rel_paths.append(str(rel).replace('\\', '/'))
            except ValueError:
                # If outside, just store name
                rel_paths.append(p.name)

        self.selected_files = rel_paths
        names = ", ".join(Path(p).name for p in rel_paths)
        if not names:
            names = "none"
        self.context_label.configure(text=f"Context: {names}")

    def _copy_panel_text(self, textbox: ctk.CTkTextbox):
        """Copy entire content of a panel."""
        try:
            content = textbox.get("1.0", "end-1c").strip()
            if not content:
                return
            self.clipboard_clear()
            self.clipboard_append(content)
            self._flash_status("Copied to clipboard!", "ok")
        except Exception:
            pass

    def _copy_selected_from_box(self, textbox: ctk.CTkTextbox):
        """Copy selected text from a specific textbox."""
        try:
            selected = textbox.get("sel.first", "sel.last")
        except tk.TclError:
            return
        if not selected:
            return
        self.clipboard_clear()
        self.clipboard_append(selected)
        self._flash_status("Copied to clipboard!", "ok")

    def _select_all_in_box(self, textbox: ctk.CTkTextbox):
        """Select all text in a specific textbox."""
        state = textbox.cget("state")
        if state == "disabled":
            textbox.configure(state="normal")
        textbox.tag_add("sel", "1.0", "end-1c")
        textbox.see("1.0")
        textbox.focus_set()
        if state == "disabled":
            textbox.configure(state="disabled")

    def _on_copy(self, event, textbox: ctk.CTkTextbox):
        self._copy_selected_from_box(textbox)
        return "break"

    def _on_select_all(self, event, textbox: ctk.CTkTextbox):
        self._select_all_in_box(textbox)
        return "break"

    def _show_context_menu(self, event, textbox: ctk.CTkTextbox):
        try:
            textbox._context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            textbox._context_menu.grab_release()


def main():
    app = ThurteaAssistantApp()
    app.mainloop()


if __name__ == "__main__":
    main()
