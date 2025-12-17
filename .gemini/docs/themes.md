# Themes

> Source: [https://geminicli.com/docs/cli/themes](https://geminicli.com/docs/cli/themes)

## Available Themes

- `dark` - Dark background (default)
- `light` - Light background
- `monokai` - Monokai colors
- `solarized-dark` - Solarized dark
- `solarized-light` - Solarized light

## Setting Theme

### Configuration
```json
{
  "theme": "dark"
}
```

### Slash Command
```
/theme dark
```

## Customization

```json
{
  "theme": "custom",
  "colors": {
    "primary": "#4285f4",
    "secondary": "#34a853",
    "error": "#ea4335",
    "background": "#1e1e1e"
  }
}
```

## Disabling Colors

```json
{
  "colors": false
}
```

Or for piping:
```bash
gemini --no-color "Query" | less
```

## Related Pages

- [Settings](settings.md) - All settings
- [Keyboard Shortcuts](keyboard-shortcuts.md) - UI customization
