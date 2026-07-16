from pathlib import Path


def find_project_root(start: Path | None = None) -> Path:
    current = (start or Path.cwd()).resolve()
    for candidate in [current, *current.parents]:
        if (candidate / "pyproject.toml").exists():
            return candidate
    raise FileNotFoundError("Could not locate the repository root.")


def _parse_scalar(value: str):
    value = value.strip()
    if value.lower() in {"true", "false"}:
        return value.lower() == "true"
    try:
        return int(value)
    except ValueError:
        try:
            return float(value)
        except ValueError:
            return value.strip('"\'')


def load_settings(config_path: str | Path, project_root: Path | None = None) -> tuple[dict, Path]:
    root = project_root or find_project_root()
    path = Path(config_path)
    if not path.is_absolute():
        path = root / path
    if not path.exists():
        raise FileNotFoundError(f"Configuration file not found: {path}")

    config: dict = {}
    parents: list[tuple[int, dict]] = [(-1, config)]
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        if not raw_line.strip() or raw_line.lstrip().startswith("#"):
            continue
        indent = len(raw_line) - len(raw_line.lstrip(" "))
        key, separator, raw_value = raw_line.strip().partition(":")
        if not separator:
            raise ValueError(f"Invalid configuration line: {raw_line}")
        while parents[-1][0] >= indent:
            parents.pop()
        current = parents[-1][1]
        if raw_value.strip():
            current[key] = _parse_scalar(raw_value)
        else:
            current[key] = {}
            parents.append((indent, current[key]))
    return config, root
