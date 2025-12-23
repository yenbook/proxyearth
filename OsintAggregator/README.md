# 🔍 OSINT Aggregator

**A powerful, modular command-line OSINT (Open Source Intelligence) automation tool built with Python 3.**

OSINT Aggregator is designed to streamline reconnaissance by automating the collection of publicly available information across multiple sources. Built with a modular architecture, it's easy to extend with new data sources from repositories like [Awesome OSINT](https://github.com/jivoi/awesome-osint).

---

## 🌟 Features

- ✅ **Username Enumeration**: Check username availability across 5+ major platforms
- 📧 **Email Breach Checking**: (Coming soon) Verify if emails appear in data breaches
- 🌐 **IP Geolocation**: (Coming soon) Lookup IP addresses and reputation
- 🔄 **Modular Architecture**: Easily add new OSINT sources
- 🛡️ **Rate Limiting Protection**: Built-in delays to avoid being blocked
- 📊 **Export Results**: Save findings to JSON or CSV
- 🎨 **Beautiful CLI**: Color-coded output with progress indicators
- ⚡ **Error Handling**: Robust error handling for failed requests

---

## 📋 Table of Contents

- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [Usage Examples](#-usage-examples)
- [Features Breakdown](#-features-breakdown)
- [Adding More Sources](#-adding-more-sources)
- [Architecture](#-architecture)
- [Extending the Tool](#-extending-the-tool)
- [Troubleshooting](#-troubleshooting)
- [Legal & Ethics](#-legal--ethics)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🚀 Installation

### Prerequisites

- **Python 3.8 or higher**
- **pip** (Python package manager)
- **Internet connection**

### Step 1: Clone the Repository

```bash
cd OsintAggregator
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

Or install manually:

```bash
pip install requests beautifulsoup4 lxml
```

### Step 3: Make the Script Executable (Linux/Mac)

```bash
chmod +x scanner.py
```

---

## ⚡ Quick Start

### Basic Username Search

```bash
python scanner.py --username johndoe
```

### Search with Export

```bash
python scanner.py --username alice --export json
```

### Check Specific Platforms

```bash
python scanner.py --username bob --platforms GitHub Reddit Twitter/X
```

---

## 📖 Usage Examples

### 1. Username Enumeration

Check if a username exists across all configured platforms:

```bash
python scanner.py --username johndoe
```

**Output:**
```
🔍 Checking username 'johndoe' across 5 platforms...

[1/5] Checking GitHub... ✅ FOUND - https://github.com/johndoe
[2/5] Checking Instagram... ❌ Not found
[3/5] Checking Twitter/X... ✅ FOUND - https://twitter.com/johndoe
[4/5] Checking Reddit... ✅ FOUND - https://www.reddit.com/user/johndoe
[5/5] Checking Medium... ❌ Not found

📊 SUMMARY
Total platforms checked: 5
✅ Username found on: 3 platform(s)
❌ Not found on: 2 platform(s)
⚠️  Errors: 0
Success rate: 100.0%
```

### 2. Export Results to JSON

```bash
python scanner.py --username alice --export json
```

This creates a timestamped JSON file: `osint_results_alice_20231215_143022.json`

### 3. Export Results to CSV

```bash
python scanner.py --username bob --export csv --output bob_results.csv
```

### 4. Check Specific Platforms Only

```bash
python scanner.py --username charlie --platforms GitHub LinkedIn
```

### 5. Email Breach Check (Coming Soon)

```bash
python scanner.py --email user@example.com
```

### 6. IP Address Lookup (Coming Soon)

```bash
python scanner.py --ip 8.8.8.8
```

### 7. Verbose Mode for Debugging

```bash
python scanner.py --username dave --verbose
```

---

## 🔧 Features Breakdown

### ✅ Current Features

#### 1. Username Enumeration

The tool checks username availability across these platforms:

| Platform | URL Pattern | Status |
|----------|-------------|--------|
| GitHub | `https://github.com/{username}` | ✅ Active |
| Instagram | `https://www.instagram.com/{username}/` | ✅ Active |
| Twitter/X | `https://twitter.com/{username}` | ✅ Active |
| Reddit | `https://www.reddit.com/user/{username}` | ✅ Active |
| Medium | `https://medium.com/@{username}` | ✅ Active |

**Error Handling:**
- ✅ Request timeouts (10s default)
- ✅ Connection errors
- ✅ Rate limiting (1s delay between requests)
- ✅ Too many redirects
- ✅ Generic request exceptions

### 🚧 Coming Soon

#### 2. Email Breach Checking

**Planned integrations:**
- Have I Been Pwned (HIBP) API
- DeHashed
- IntelX

#### 3. IP Address Lookup

**Planned integrations:**
- IPinfo.io
- AbuseIPDB
- Shodan

---

## 📦 Adding More Sources

The tool is designed to be **easily extensible**. Here's how to add more platforms to username enumeration:

### Method 1: Edit `modules/username_enum.py`

Open `modules/username_enum.py` and locate the `PLATFORMS` dictionary (around line 35):

```python
PLATFORMS = {
    "GitHub": {
        "url": "https://github.com/{username}",
        "found_code": 200,
        "not_found_code": 404,
        "method": "GET"
    },
    # ADD YOUR PLATFORM HERE:
    "LinkedIn": {
        "url": "https://www.linkedin.com/in/{username}",
        "found_code": 200,
        "not_found_code": 404,
        "method": "GET"
    },
}
```

**Steps:**
1. Find the platform's URL pattern (e.g., from [Awesome OSINT](https://github.com/jivoi/awesome-osint))
2. Determine the HTTP status codes for "found" (usually 200) and "not found" (usually 404)
3. Add a new entry to the `PLATFORMS` dictionary
4. Save and test!

### Method 2: Create a Configuration File (Advanced)

For advanced users, you can create a `config/platforms.json` file:

```json
{
  "TikTok": {
    "url": "https://www.tiktok.com/@{username}",
    "found_code": 200,
    "not_found_code": 404
  }
}
```

Then modify `username_enum.py` to load platforms from this JSON file.

---

## 🏗️ Architecture

### Project Structure

```
OsintAggregator/
├── scanner.py              # Main CLI entry point
├── modules/                # Modular OSINT components
│   ├── __init__.py
│   ├── username_enum.py    # Username enumeration module
│   ├── email_breach.py     # (Coming soon) Email breach checker
│   └── ip_lookup.py        # (Coming soon) IP geolocation
├── config/                 # Configuration files
│   └── platforms.json      # (Optional) Platform definitions
├── utils/                  # Utility functions
│   └── __init__.py
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

### How It Works

```
User Input (CLI)
      ↓
scanner.py (Orchestrator)
      ↓
Validates Input
      ↓
Routes to Module:
  ├─ username_enum.py → Checks multiple platforms
  ├─ email_breach.py  → Checks breach databases
  └─ ip_lookup.py     → Performs IP lookup
      ↓
Returns Results
      ↓
Displays Summary
      ↓
(Optional) Export to JSON/CSV
```

---

## 🛠️ Extending the Tool

### Adding a New Module (Email Breach Checker Example)

#### Step 1: Create the Module File

Create `modules/email_breach.py`:

```python
import requests

class EmailBreachChecker:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.api_url = "https://haveibeenpwned.com/api/v3/breachedaccount/{email}"

    def check_email(self, email: str):
        headers = {"hibp-api-key": self.api_key}
        response = requests.get(
            self.api_url.format(email=email),
            headers=headers
        )
        if response.status_code == 200:
            return {"found": True, "breaches": response.json()}
        elif response.status_code == 404:
            return {"found": False, "breaches": []}
        else:
            return {"error": f"HTTP {response.status_code}"}
```

#### Step 2: Import in `scanner.py`

Add to the imports:

```python
from modules.email_breach import EmailBreachChecker
```

#### Step 3: Update the `scan_email` Method

Replace the placeholder in `scanner.py`:

```python
def scan_email(self, email: str) -> Dict:
    print(f"\n{Colors.HEADER}📧 EMAIL BREACH CHECK{Colors.ENDC}")
    print(f"{Colors.BLUE}Target: {email}{Colors.ENDC}")

    checker = EmailBreachChecker(api_key="YOUR_API_KEY")
    result = checker.check_email(email)

    if result.get("found"):
        print(f"{Colors.FAIL}⚠️  Email found in {len(result['breaches'])} breach(es)!{Colors.ENDC}")
    else:
        print(f"{Colors.GREEN}✅ Email not found in known breaches{Colors.ENDC}")

    return result
```

#### Step 4: Test

```bash
python scanner.py --email test@example.com
```

---

## 🐛 Troubleshooting

### Issue: `ModuleNotFoundError: No module named 'requests'`

**Solution:**
```bash
pip install -r requirements.txt
```

### Issue: "Connection failed - site may be blocking requests"

**Solution:**
- Some websites block automated requests
- The tool already uses a realistic User-Agent
- Try increasing the delay: Edit `username_enum.py` and change `delay=1.0` to `delay=2.0`

### Issue: "Request timed out"

**Solution:**
- Check your internet connection
- Increase timeout: `UsernameEnumerator(timeout=20)`

### Issue: Too many 429 (Rate Limited) errors

**Solution:**
- Reduce the number of platforms checked
- Increase delay between requests in `username_enum.py`

---

## ⚖️ Legal & Ethics

### ⚠️ IMPORTANT DISCLAIMER

This tool is for **educational and authorized security research purposes only**.

**Legal Guidelines:**
- ✅ **DO**: Use on your own accounts and systems
- ✅ **DO**: Use for authorized penetration testing
- ✅ **DO**: Use for OSINT training and CTF competitions
- ❌ **DON'T**: Use for unauthorized access
- ❌ **DON'T**: Use for harassment or stalking
- ❌ **DON'T**: Violate websites' Terms of Service
- ❌ **DON'T**: Use for malicious purposes

**Responsible Usage:**
- Always respect `robots.txt` and API rate limits
- Use delays between requests (already implemented)
- Do not overload servers with excessive requests
- Comply with GDPR, CCPA, and local privacy laws

**The authors are not responsible for misuse of this tool.**

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

### Ways to Contribute

1. **Add New Platforms**: Submit PRs with new platform integrations
2. **Implement Email/IP Modules**: Help build the email and IP lookup features
3. **Improve Error Handling**: Enhance robustness
4. **Write Tests**: Add unit tests for modules
5. **Documentation**: Improve this README or add code comments

### Contribution Guidelines

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes
4. Test thoroughly
5. Commit: `git commit -m 'Add amazing feature'`
6. Push: `git push origin feature/amazing-feature`
7. Open a Pull Request

---

## 📝 Example Output

```
======================================================================
   ___  ____ ___ _   _ _____      _
  / _ \/ ___|_ _| \ | |_   _|    / \   __ _  __ _ _ __ ___  __ _  __ _
 | | | \___ \| ||  \| | | |     / _ \ / _` |/ _` | '__/ _ \/ _` |/ _` |
 | |_| |___) | || |\  | | |    / ___ \ (_| | (_| | | |  __/ (_| | (_| |
  \___/|____/___|_| \_| |_|   /_/   \_\__, |\__, |_|  \___|\__, |\__,_|
                                       |___/ |___/          |___/
    Open Source Intelligence Automation Tool v1.0.0
======================================================================

🔍 USERNAME ENUMERATION
Target: johndoe

🔍 Checking username 'johndoe' across 5 platforms...

[1/5] Checking GitHub... ✅ FOUND - https://github.com/johndoe
[2/5] Checking Instagram... ❌ Not found
[3/5] Checking Twitter/X... ✅ FOUND - https://twitter.com/johndoe
[4/5] Checking Reddit... ✅ FOUND - https://www.reddit.com/user/johndoe
[5/5] Checking Medium... ❌ Not found

======================================================================
📊 SUMMARY
======================================================================
Total platforms checked: 5
✅ Username found on: 3 platform(s)
❌ Not found on: 2 platform(s)
⚠️  Errors: 0
Success rate: 100.0%

Found on:
  • GitHub: https://github.com/johndoe
  • Twitter/X: https://twitter.com/johndoe
  • Reddit: https://www.reddit.com/user/johndoe

✅ Results exported to: osint_results_johndoe_20231215_143530.json

✅ Scan completed successfully!
```

---

## 🔗 Resources

### OSINT Resources
- [Awesome OSINT](https://github.com/jivoi/awesome-osint) - Curated list of OSINT tools and resources
- [OSINT Framework](https://osintframework.com/) - Collection of OSINT tools
- [Have I Been Pwned](https://haveibeenpwned.com/) - Check if emails are in breaches

### Python Resources
- [Requests Documentation](https://requests.readthedocs.io/)
- [BeautifulSoup Documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)

---

## 📄 License

This project is licensed under the **MIT License**.

```
MIT License

Copyright (c) 2024 OSINT Aggregator Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 👨‍💻 Author

**Senior Python Developer with Cybersecurity Background**

Built with ❤️ for the OSINT community.

---

## 🙏 Acknowledgments

- Inspired by the [Awesome OSINT](https://github.com/jivoi/awesome-osint) repository
- Thanks to all platform providers for public APIs
- OSINT community for tools and resources

---

**⭐ If you find this tool useful, please give it a star on GitHub!**

---

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/yenbook/proxyearth/issues)
- **Discussions**: Open a GitHub Discussion
- **Security**: Report security issues privately

---

*Last updated: December 2024*
