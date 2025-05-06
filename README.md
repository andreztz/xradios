# Xradios 📻

> "Search, bookmark, and stream internet radio stations directly from your terminal."

[![PyPI Version](https://img.shields.io/pypi/v/xradios?color=blue)](https://pypi.org/project/xradios/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)

**Xradios** is a terminal tool to discover and streaming radio stations worldwide.

## Features ✨

- **Search**: Find radio stations by name, genre, country, language or other criteria.
- **Stream**: Play radio stations directly in your terminal.
- **Interactive Interface**: Navigate and control playback with keyboard shortcuts.
- **Bookmarks**: Save stations for quick access. (TODO)

## Installation 🛠️

### Prerequisites

- Python 3.8 or higher
- `mpv` or `libmpv` for audio playback

### Using pipx (recommended)

```bash
pipx install xradios
```

### Alternative: Install via pip
```bash
pip install --user xradios
```

## Usage 🚀

Start the server:

```bash
xradiosd
```

Launch the interactive interface:

```
xradios
```

### Commands

- **Open command line**: Press `:`
- **Navigate**: Use `Ctrl + UP`/`Ctrl + DOWN` to move focus.
- **Search for stations**: `search tag=rock limit=100 order=votes`
- **Play a station**: Select a station with `UP`/`DOWN` and press `ENTER`.
- **Exit**: Press `Ctrl + q`

Press `?` to see a complete list of shortcuts and commands.


## Development Setup 💻

1. Clone the repository and navigate into project directory:

```bash
git clone git@github.com:andreztz/xradios.git
cd xradios
```

2. Install development dependencies using the following command:

```bash
uv sync --dev
```

3. Start the xradios server by running:

```
xradiosd
```

4. Open a new terminal, and run textual console to monitor log messsages:

```
textual console
```

5. In another terminal run xradios application in development mode:

```
textual run --dev xradios
```

6. Run tests:

```bash
pytest
```

## Contributing 🤝

Contributions are welcome! Please open an issue or submit a pull request.  
See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## Troubleshooting 🔧

- **No audio?** Ensure `mpv` or `libmpv` is installed and accessible in you PATH.

## Meta 📬

André P. Santos – [@ztzandre](https://twitter.com/ztzandre) – andreztz@gmail.com

Distributed under the MIT license. See [LICENSE](LICENSE) for details.

GitHub: [https://github.com/andreztz/xradios](https://github.com/andreztz/xradios)
