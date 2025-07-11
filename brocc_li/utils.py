import json
from pathlib import Path
from typing import Any, Dict


def get_config(path: Path = Path(".env/config.json")) -> Dict[str, Any]:
    """Load JSON configuration (API keys, etc) from file."""
    try:
        data = json.loads(path.read_text())
    except FileNotFoundError:
        raise FileNotFoundError(f"Configuration file not found at {path}")
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in configuration file: {e}")
    return data
