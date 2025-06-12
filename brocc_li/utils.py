import json


def get_config(path: str = ".env/config.json") -> dict:
    try:
        with open(path, "r") as f:
            return json.load(f)

    except FileNotFoundError:
        raise FileNotFoundError(f"Configuration file not found at: {path}")

    except json.JSONDecodeError as e:
        raise json.JSONDecodeError(
            f"Invalid JSON in configuration file: {path}", e.doc, e.pos
        )
