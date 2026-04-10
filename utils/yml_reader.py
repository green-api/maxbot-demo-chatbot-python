import os, yaml

try:
    with open(os.path.join("assets", "strings.yaml"), "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
except Exception as e:
    raise RuntimeError(f"Failed to load strings.yaml: {e}")

def t(lang: str, path: str) -> str:
    parts = path.split(".")
    current = data

    for part in parts:
        if isinstance(current, dict) and part in current:
            current = current[part]
        else:
            raise KeyError(f"Key '{path}' (failed at '{part}') not found in strings.yaml")

    if isinstance(current, str):
        return current

    if isinstance(current, dict):
        for key in [lang, "ru", "en"]:
            val = current.get(key)
            if isinstance(val, str):
                return val
    
    return ""