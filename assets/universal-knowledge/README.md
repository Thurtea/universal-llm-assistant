# Universal Knowledge Assistant - Assets

## Logo Files

- **LLM-Assistant-Logo.png** - Main logo (high resolution)
- **favicon.ico** - Windows icon for shortcuts and taskbar
- **android-chrome-192x192.png** - Android home screen icon
- **android-chrome-512x512.png** - Android high-res icon
- **apple-touch-icon.png** - iOS home screen icon
- **favicon-16x16.png** - Small favicon
- **favicon-32x32.png** - Standard favicon

## Usage

These assets are automatically used by:
- `first_run_setup.pyw` - Setup wizard logo
- `gui_assistant.py` - Main application icon
- Desktop shortcuts - Taskbar/shortcut icon
- Browser bookmarks (if used as PWA)

## Customization

To use your own logo:
1. Replace `LLM-Assistant-Logo.png` with your logo (512x512 recommended)
2. Run `python generate_logo.py` to regenerate all icon sizes
3. Or manually replace individual icon files

## Icon Generation

The setup wizard automatically checks for these icons and uses them.
If `favicon.ico` exists, it uses it directly.
Otherwise, it can generate icons from `LLM-Assistant-Logo.png`.
