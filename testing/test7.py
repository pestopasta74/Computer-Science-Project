import json
import tkinter as tk
from tkinter import ttk
import os
import sys
from typing import Dict, Any, Optional

class ResponsiveThemedWindow(tk.Tk):
    def __init__(
        self,
        title: str = "Application",
        width: int = 800,
        height: int = 600,
        style_config: Optional[str] = None,
        settings_config: Optional[str] = None
    ):
        """
        Initialize a responsive, themed Tkinter window with system theme and accessibility support.

        Args:
            title (str): Window title
            width (int): Initial window width
            height (int): Initial window height
            style_config (str, optional): Path to style JSON configuration
            settings_config (str, optional): Path to settings JSON configuration
        """
        super().__init__()

        # Default configurations
        self.default_style = {
            "background": "#FFFFFF",
            "foreground": "#000000",
            "font": ("Arial", 10),
            "dark_mode": {
                "background": "#1E1E1E",
                "foreground": "#FFFFFF"
            }
        }

        self.default_settings = {
            "font": "Arial",
            "text_size": 10,
            "high_contrast": False
        }

        # Load style configuration
        self.style_config = self._load_config(style_config, self.default_style)
        self.settings_config = self._load_config(settings_config, self.default_settings)

        # Configure window
        self.title(title)
        self.geometry(f"{width}x{height}")

        # System theme detection and handling
        self._detect_system_theme()
        self._apply_theme()

        # Bind theme change events
        self.bind_system_theme_change()

    def _load_config(self, config_path: Optional[str], default_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Load JSON configuration with fallback to default config.

        Args:
            config_path (str, optional): Path to JSON configuration file
            default_config (dict): Default configuration dictionary

        Returns:
            dict: Loaded or default configuration
        """
        try:
            if config_path and os.path.exists(config_path):
                with open(config_path, 'r') as f:
                    config = json.load(f)
                return {**default_config, **config}
        except (json.JSONDecodeError, IOError):
            print(f"Warning: Could not load config from {config_path}")

        return default_config

    def _detect_system_theme(self) -> str:
        """
        Detect the current system theme.

        Returns:
            str: Current system theme ('light' or 'dark')
        """
        # Placeholder for system theme detection
        # In a real implementation, this would use platform-specific methods
        # For now, we'll use a simple environment variable or default to light
        return os.environ.get('THEME', 'light')

    def _apply_theme(self):
        """
        Apply the appropriate theme based on system settings and configuration.
        """
        theme = self._detect_system_theme()

        # Apply high contrast if enabled
        if self.settings_config.get('high_contrast', False):
            self.configure(
                bg='black',
                fg='yellow',
                font=(
                    self.settings_config.get('font', 'Arial'),
                    int(self.settings_config.get('text_size', 12))
                )
            )
            return

        # Apply dark or light theme
        if theme == 'dark':
            bg = self.style_config.get('dark_mode', {}).get('background', '#1E1E1E')
            fg = self.style_config.get('dark_mode', {}).get('foreground', '#FFFFFF')
        else:
            bg = self.style_config.get('background', '#FFFFFF')
            fg = self.style_config.get('foreground', '#000000')

        # Configure window and style
        self.configure(
            bg=bg,
            font=(
                self.settings_config.get('font', 'Arial'),
                int(self.settings_config.get('text_size', 10))
            )
        )

        # Configure ttk style for consistency
        style = ttk.Style()
        style.configure('TFrame', background=bg)
        style.configure('TLabel', background=bg, foreground=fg)
        style.configure('TButton', background=bg, foreground=fg)

    def bind_system_theme_change(self):
        """
        Bind method to handle system theme changes.
        This is a placeholder and would need platform-specific implementation.
        """
        # In a real implementation, this would use platform-specific
        # methods to detect and respond to theme changes
        pass

    def create_widget(self, widget_type, **kwargs):
        """
        Create a widget with theme-aware defaults.

        Args:
            widget_type (tk.Widget): Tkinter widget class
            **kwargs: Widget configuration parameters

        Returns:
            tk.Widget: Configured widget
        """
        # Merge theme defaults with provided kwargs
        theme_defaults = {
            'bg': self.style_config.get('background', '#FFFFFF'),
            'fg': self.style_config.get('foreground', '#000000'),
            'font': self.settings_config.get('font', 'Arial')
        }
        theme_defaults.update(kwargs)

        return widget_type(self, **theme_defaults)

# Example usage
if __name__ == "__main__":
    # Example settings and style JSON files
    example_settings = {
        "font": "Helvetica",
        "text_size": 12,
        "high_contrast": False
    }

    example_style = {
        "background": "#F0F0F0",
        "foreground": "#333333",
        "dark_mode": {
            "background": "#2C2C2C",
            "foreground": "#E0E0E0"
        }
    }

    # Write example config files
    os.makedirs('config', exist_ok=True)

    with open('config/settings.json', 'w') as f:
        json.dump(example_settings, f, indent=4)

    with open('config/style.json', 'w') as f:
        json.dump(example_style, f, indent=4)

    # Create window
    app = ResponsiveThemedWindow(
        title="Themed Application",
        width=1024,
        height=768,
        style_config='config/style.json',
        settings_config='config/settings.json'
    )

    # Add a label to demonstrate theming
    label = app.create_widget(tk.Label, text="Hello, Themed World!")
    label.pack(expand=True)

    app.mainloop()