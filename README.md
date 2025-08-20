![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

# Red Team Loot Tracker (CLI)

Simple terminal tool to catalog credentials, host artifacts, and sensitive finds.
Stores data in an **encrypted JSON vault** (Fernet).

## Commands
```bash
python -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt
python loot.py init
python loot.py add --type cred --name "db-admin" --value "u:foo p:bar" --tags prod,db
python loot.py list
python loot.py search --query prod
python loot.py export --format csv --out loot.csv
```
Key is stored locally in `vault.key`. Keep it safe.

## Data & Samples
- Runtime data (`loot.json`, `loot.csv`, `vault.*`) is **gitignored** to avoid committing secrets.
- See **samples/sample_loot.json** and **samples/sample_loot.csv** for sanitized examples (all values are redacted).
