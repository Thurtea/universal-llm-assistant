"""
LLM Assistant Core Engine
Manages conversation context, file loading, and Ollama integration
"""

import ollama
from pathlib import Path
from typing import List, Dict, Optional
import json

class LLMAssistant:
    def __init__(
        self,
        model: str = None,
        codebase_path: str = "../aethermud-code",
        context_window: int = 16384
    ):
        import yaml
        from pathlib import Path
        config_path = Path(__file__).parent / "config.yaml"
        with open(config_path, "r", encoding="utf-8") as f:
            self.config = yaml.safe_load(f)
        self.model = model or self.config.get("models", {}).get("default", "qwen2.5-coder:3b")
        self.app_name = self.config.get("assistant", {}).get("name", "Universal Knowledge Assistant")
        self.codebase_path = Path(codebase_path)
        self.context_window = context_window
        self.conversation_history = []
        self.loaded_files = {}
        
    def load_file_context(self, file_path: str, max_lines: int = 300) -> str:
        """Load file content for context"""
        # Normalize path separators to forward slashes
        normalized_path = file_path.replace('\\', '/')
        full_path = self.codebase_path / normalized_path
        
        if not full_path.exists():
            return f"Error: File {file_path} not found"
            
        with open(full_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()[:max_lines]
            
        self.loaded_files[file_path] = ''.join(lines)
        return self.loaded_files[file_path]
    
    def query(self, question: str, files: List[str] = None) -> str:
        """Send query to Ollama with context"""
        context = ""
        
        # Load file contexts
        if files:
            for file_path in files:
                content = self.load_file_context(file_path)
                context += f"\n\n=== File: {file_path} ===\n{content}"
        
        # Build prompt
        prompt = f"""You are a helpful AI coding assistant for {self.app_name} development.
    {self.app_name} is a Rifts-themed MUD built on Evennia framework in Python.

    Context files:
    {context}

    Question: {question}

    Provide a clear, code-focused answer. Reference specific lines when relevant."""

        # Query Ollama
        response = ollama.chat(
            model=self.model,
            messages=[{'role': 'user', 'content': prompt}]
        )
        
        return response['message']['content']
    
    def chat(self, message: str) -> str:
        """Conversational interface with history"""
        self.conversation_history.append({
            'role': 'user',
            'content': message
        })
        
        response = ollama.chat(
            model=self.model,
            messages=self.conversation_history
        )
        
        assistant_message = response['message']['content']
        self.conversation_history.append({
            'role': 'assistant',
            'content': assistant_message
        })
        
        return assistant_message
