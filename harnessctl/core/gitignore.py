from __future__ import annotations

from pathlib import Path


_GITIGNORES: dict[str, str] = {
    "go": """\
# Go
*.exe
*.exe~
*.dll
*.so
*.dylib
*.test
*.out
vendor/
go.sum

# Build output
/bin/
/dist/
/build/

# Environment
.env
.env.local
.env.*.local
*.pem
*.key

# IDE
.idea/
.vscode/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Test coverage
*.cover
coverage.txt
coverage.html

# Docker
docker-compose.override.yml

# Logs
*.log
logs/
""",
    "node": """\
# Dependencies
node_modules/

# Build output
dist/
build/
.next/
.nuxt/
out/

# Environment
.env
.env.local
.env.*.local
*.pem
*.key

# IDE
.idea/
.vscode/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Logs
*.log
logs/
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# Test coverage
coverage/
.nyc_output/

# Docker
docker-compose.override.yml
""",
    "python": """\
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
*.egg
*.egg-info/
dist/
build/
.eggs/
pip-wheel-metadata/

# Virtual environments
venv/
.venv/
env/
.env/

# Environment
.env.local
*.pem
*.key

# IDE
.idea/
.vscode/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Test
.pytest_cache/
.coverage
htmlcov/
tox.ini

# Docker
docker-compose.override.yml

# Logs
*.log
logs/
""",
    "generic": """\
# Environment
.env
.env.local
*.pem
*.key

# IDE
.idea/
.vscode/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Build output
dist/
build/
bin/

# Logs
*.log
logs/

# Docker
docker-compose.override.yml
""",
}

_LANGUAGE_ALIASES: dict[str, str] = {
    "golang": "go",
    "nodejs": "node",
    "node.js": "node",
    "javascript": "node",
    "typescript": "node",
    "py": "python",
    "python3": "python",
}


def normalize_language(language: str) -> str:
    key = language.strip().lower()
    return _LANGUAGE_ALIASES.get(key, key)


def _resolve_language(language: str) -> str:
    normalized = normalize_language(language)
    if normalized not in _GITIGNORES:
        normalized = "generic"
    return normalized


def get_gitignore(language: str) -> str:
    return _GITIGNORES[_resolve_language(language)]


def supported_languages() -> list[str]:
    return sorted(_GITIGNORES.keys())


def validate_gitignore(path: Path, language: str) -> dict:
    if not path.exists():
        return {"valid": False, "reason": ".gitignore does not exist."}
    content = path.read_text(encoding="utf-8")
    normalized = _resolve_language(language)
    required_patterns: list[str]
    if normalized == "go":
        required_patterns = ["*.exe", "vendor/", ".env", ".idea/", ".vscode/"]
    elif normalized == "node":
        required_patterns = ["node_modules/", "dist/", ".env", ".idea/", ".vscode/"]
    elif normalized == "python":
        required_patterns = ["__pycache__/", ".venv/", ".env", ".idea/", ".vscode/"]
    else:
        required_patterns = [".env", ".idea/", ".vscode/"]
    missing = [p for p in required_patterns if p not in content]
    return {
        "valid": not missing,
        "missing_patterns": missing,
        "language": normalized,
    }


def generate_gitignore(root: Path, language: str) -> dict:
    target = root / ".gitignore"
    resolved = _resolve_language(language)
    if target.exists():
        existing = target.read_text(encoding="utf-8")
        expected = get_gitignore(language)
        if existing.strip() == expected.strip():
            return {
                "valid": True,
                "path": str(target),
                "action": "unchanged",
                "language": resolved,
            }
        return {
            "valid": False,
            "path": str(target),
            "action": "exists",
            "reason": (
                ".gitignore already exists with different content. "
                "Review manually or remove it before generating."
            ),
        }
    content = get_gitignore(language)
    target.write_text(content, encoding="utf-8")
    return {
        "valid": True,
        "path": str(target),
        "action": "created",
        "language": resolved,
    }
