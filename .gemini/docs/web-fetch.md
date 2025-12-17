# Web Fetch Tool

> Source: [https://geminicli.com/docs/tools/web-fetch](https://geminicli.com/docs/tools/web-fetch)

## Overview

Fetch content from web pages.

## Usage

```
> Fetch the content from ableton.com/help
[Fetches and returns page content]
```

## Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `url` | string | URL to fetch |
| `headers` | object | Optional headers |
| `timeout` | number | Timeout in ms |

## Response

Returns:
- Page content (HTML or text)
- Status code
- Headers

## Limitations

- No JavaScript execution
- Public pages only
- Size limits apply

## ableton-mcp Usage

```
> Fetch the Ableton manual page for Compressor
> Get the content from musicradar.com/techno-tutorial
```

## Related Pages

- [Web Search Tool](web-search.md) - Search web
- [Tools](tools.md) - All tools
