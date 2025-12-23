# 🚀 Quick Start Guide

Get started with OSINT Aggregator in under 5 minutes!

## Installation

### 1. Install Python Dependencies

```bash
cd OsintAggregator
pip install -r requirements.txt
```

### 2. Run Your First Scan

```bash
python scanner.py --username github
```

That's it! You should see results showing where the username "github" was found.

## Basic Usage

### Check a Username

```bash
python scanner.py --username johndoe
```

### Check Specific Platforms Only

```bash
python scanner.py --username alice --platforms GitHub Reddit
```

### Export Results to JSON

```bash
python scanner.py --username bob --export json
```

### Export Results to CSV

```bash
python scanner.py --username charlie --export csv
```

## What's Next?

- 📖 Read the full [README.md](README.md) for detailed documentation
- 🔧 Learn how to [add more platforms](README.md#-adding-more-sources)
- 💻 See [examples.py](examples.py) for programmatic usage
- 🚀 Extend the tool with email and IP lookup modules

## Common Commands

```bash
# Get help
python scanner.py --help

# Verbose mode for debugging
python scanner.py --username test --verbose

# Hide banner
python scanner.py --username test --no-banner

# Custom output filename
python scanner.py --username test --export json --output my_results.json
```

## Troubleshooting

**Problem:** `ModuleNotFoundError: No module named 'requests'`

**Solution:** Install dependencies:
```bash
pip install -r requirements.txt
```

---

**Problem:** "Connection failed - site may be blocking requests"

**Solution:** Some sites block automated requests. This is normal. The tool will continue checking other platforms.

---

For more help, see the [README.md](README.md) or open an issue on GitHub.
