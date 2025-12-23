#!/usr/bin/env python3
"""
OSINT Aggregator - Open Source Intelligence Automation Tool
============================================================
A command-line interface (CLI) tool that accepts a single input (email, username, or IP)
and queries multiple public OSINT sources to return a comprehensive summary.

Author: Senior Python Developer with Cybersecurity background
Version: 1.0.0
License: MIT

FEATURES:
- Username enumeration across major platforms
- Email breach checking (extensible)
- IP address geolocation (extensible)
- Modular architecture for easy extension
- Comprehensive error handling
- Rate limiting protection
- Export results to JSON/CSV

USAGE:
    python scanner.py --username <username>
    python scanner.py --email <email>
    python scanner.py --ip <ip_address>
    python scanner.py --username <username> --export json
"""

import argparse
import sys
import json
import csv
from datetime import datetime
from typing import Dict, List, Optional
import os

# Import our modular components
# Note: Make sure modules directory is in PYTHONPATH or use relative imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from modules.username_enum import UsernameEnumerator


class Colors:
    """ANSI color codes for terminal output"""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class OsintAggregator:
    """
    Main OSINT Aggregator class that orchestrates different OSINT modules.
    """

    def __init__(self, verbose: bool = False):
        """
        Initialize the OSINT Aggregator.

        Args:
            verbose (bool): Enable verbose output for debugging
        """
        self.verbose = verbose
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "input_type": None,
            "input_value": None,
            "username_enum": None,
            "email_check": None,
            "ip_lookup": None
        }

    def print_banner(self):
        """Print the tool banner."""
        banner = f"""
{Colors.CYAN}{'='*70}
   ___  ____ ___ _   _ _____      _
  / _ \/ ___|_ _| \ | |_   _|    / \   __ _  __ _ _ __ ___  __ _  __ _
 | | | \___ \| ||  \| | | |     / _ \ / _` |/ _` | '__/ _ \/ _` |/ _` |
 | |_| |___) | || |\  | | |    / ___ \ (_| | (_| | | |  __/ (_| | (_| |
  \___/|____/___|_| \_| |_|   /_/   \_\__, |\__, |_|  \___|\__, |\__,_|
                                       |___/ |___/          |___/
{Colors.ENDC}{Colors.BOLD}    Open Source Intelligence Automation Tool v1.0.0{Colors.ENDC}
{Colors.CYAN}{'='*70}{Colors.ENDC}
        """
        print(banner)

    def scan_username(self, username: str, platforms: Optional[List[str]] = None) -> Dict:
        """
        Perform username enumeration across platforms.

        Args:
            username (str): Username to search for
            platforms (list, optional): Specific platforms to check

        Returns:
            dict: Enumeration results
        """
        print(f"\n{Colors.HEADER}🔍 USERNAME ENUMERATION{Colors.ENDC}")
        print(f"{Colors.BLUE}Target: {username}{Colors.ENDC}")

        try:
            enumerator = UsernameEnumerator(timeout=10, delay=1.0)
            results = enumerator.enumerate_all(username, platforms)
            summary = enumerator.get_summary(results)
            enumerator.close()

            # Store results
            self.results["input_type"] = "username"
            self.results["input_value"] = username
            self.results["username_enum"] = {
                "results": results,
                "summary": summary
            }

            # Print summary
            self._print_username_summary(summary, results)

            return {"status": "success", "data": results, "summary": summary}

        except Exception as e:
            error_msg = f"Username enumeration failed: {str(e)}"
            print(f"\n{Colors.FAIL}❌ ERROR: {error_msg}{Colors.ENDC}")

            if self.verbose:
                import traceback
                print(f"\n{Colors.WARNING}Traceback:{Colors.ENDC}")
                traceback.print_exc()

            return {"status": "error", "message": error_msg}

    def _print_username_summary(self, summary: Dict, results: List[Dict]):
        """Print formatted username enumeration summary."""
        print(f"\n{Colors.CYAN}{'='*70}")
        print(f"📊 SUMMARY")
        print(f"{'='*70}{Colors.ENDC}")

        print(f"Total platforms checked: {summary['total_checked']}")
        print(f"{Colors.GREEN}✅ Username found on: {summary['found_on']} platform(s){Colors.ENDC}")
        print(f"{Colors.WARNING}❌ Not found on: {summary['not_found']} platform(s){Colors.ENDC}")
        print(f"{Colors.FAIL}⚠️  Errors: {summary['errors']}{Colors.ENDC}")
        print(f"Success rate: {summary['success_rate']}%")

        if summary['platforms_found']:
            print(f"\n{Colors.GREEN}Found on:{Colors.ENDC}")
            for platform in summary['platforms_found']:
                result = next((r for r in results if r['platform'] == platform), None)
                if result:
                    print(f"  • {platform}: {result['url']}")

    def scan_email(self, email: str) -> Dict:
        """
        Check if email appears in data breaches.

        Args:
            email (str): Email address to check

        Returns:
            dict: Breach check results

        NOTE: This is a placeholder for future implementation.
        You can integrate APIs like:
        - Have I Been Pwned (HIBP) API
        - DeHashed API
        - IntelX API
        """
        print(f"\n{Colors.HEADER}📧 EMAIL BREACH CHECK{Colors.ENDC}")
        print(f"{Colors.BLUE}Target: {email}{Colors.ENDC}")
        print(f"\n{Colors.WARNING}⚠️  Email breach checking not yet implemented.{Colors.ENDC}")
        print(f"{Colors.CYAN}To add this feature:{Colors.ENDC}")
        print("  1. Sign up for HIBP API: https://haveibeenpwned.com/API/Key")
        print("  2. Create modules/email_breach.py")
        print("  3. Implement the EmailBreachChecker class")
        print("  4. Import and call it here")

        self.results["input_type"] = "email"
        self.results["input_value"] = email
        self.results["email_check"] = {"status": "not_implemented"}

        return {"status": "not_implemented", "message": "Feature coming soon"}

    def scan_ip(self, ip_address: str) -> Dict:
        """
        Perform IP address geolocation and reputation check.

        Args:
            ip_address (str): IP address to lookup

        Returns:
            dict: IP lookup results

        NOTE: This is a placeholder for future implementation.
        You can integrate APIs like:
        - IPinfo.io
        - AbuseIPDB
        - Shodan
        """
        print(f"\n{Colors.HEADER}🌐 IP ADDRESS LOOKUP{Colors.ENDC}")
        print(f"{Colors.BLUE}Target: {ip_address}{Colors.ENDC}")
        print(f"\n{Colors.WARNING}⚠️  IP lookup not yet implemented.{Colors.ENDC}")
        print(f"{Colors.CYAN}To add this feature:{Colors.ENDC}")
        print("  1. Sign up for IPinfo.io: https://ipinfo.io/signup")
        print("  2. Create modules/ip_lookup.py")
        print("  3. Implement the IPLookup class")
        print("  4. Import and call it here")

        self.results["input_type"] = "ip"
        self.results["input_value"] = ip_address
        self.results["ip_lookup"] = {"status": "not_implemented"}

        return {"status": "not_implemented", "message": "Feature coming soon"}

    def export_results(self, format: str = "json", filename: Optional[str] = None):
        """
        Export results to JSON or CSV format.

        Args:
            format (str): Export format - 'json' or 'csv'
            filename (str, optional): Custom filename. Auto-generated if not provided.
        """
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            input_val = self.results.get("input_value", "unknown")
            filename = f"osint_results_{input_val}_{timestamp}.{format}"

        try:
            if format == "json":
                with open(filename, 'w') as f:
                    json.dump(self.results, f, indent=2)
                print(f"\n{Colors.GREEN}✅ Results exported to: {filename}{Colors.ENDC}")

            elif format == "csv":
                # Flatten results for CSV export
                with open(filename, 'w', newline='') as f:
                    if self.results.get("username_enum"):
                        results_data = self.results["username_enum"]["results"]
                        if results_data:
                            fieldnames = results_data[0].keys()
                            writer = csv.DictWriter(f, fieldnames=fieldnames)
                            writer.writeheader()
                            writer.writerows(results_data)
                            print(f"\n{Colors.GREEN}✅ Results exported to: {filename}{Colors.ENDC}")
                    else:
                        print(f"\n{Colors.WARNING}⚠️  No data to export{Colors.ENDC}")
            else:
                print(f"\n{Colors.FAIL}❌ Unsupported format: {format}{Colors.ENDC}")

        except Exception as e:
            print(f"\n{Colors.FAIL}❌ Export failed: {str(e)}{Colors.ENDC}")


def validate_username(username: str) -> bool:
    """Validate username format."""
    if not username or len(username) < 1 or len(username) > 50:
        return False
    # Basic validation - can be enhanced
    return True


def validate_email(email: str) -> bool:
    """Validate email format."""
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_ip(ip: str) -> bool:
    """Validate IP address format."""
    import re
    pattern = r'^(\d{1,3}\.){3}\d{1,3}$'
    if re.match(pattern, ip):
        parts = ip.split('.')
        return all(0 <= int(part) <= 255 for part in parts)
    return False


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="OSINT Aggregator - Automated OSINT reconnaissance tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scanner.py --username johndoe
  python scanner.py --email user@example.com
  python scanner.py --ip 8.8.8.8
  python scanner.py --username johndoe --export json
  python scanner.py --username alice --platforms GitHub Reddit Twitter/X
        """
    )

    # Input arguments (mutually exclusive)
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument(
        '-u', '--username',
        type=str,
        help='Username to search for across platforms'
    )
    input_group.add_argument(
        '-e', '--email',
        type=str,
        help='Email address to check for breaches'
    )
    input_group.add_argument(
        '-i', '--ip',
        type=str,
        help='IP address to perform lookup on'
    )

    # Optional arguments
    parser.add_argument(
        '-p', '--platforms',
        nargs='+',
        help='Specific platforms to check (default: all)'
    )
    parser.add_argument(
        '--export',
        choices=['json', 'csv'],
        help='Export results to file (json or csv)'
    )
    parser.add_argument(
        '-o', '--output',
        type=str,
        help='Custom output filename for export'
    )
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose output for debugging'
    )
    parser.add_argument(
        '--no-banner',
        action='store_true',
        help='Suppress banner output'
    )

    args = parser.parse_args()

    # Initialize aggregator
    aggregator = OsintAggregator(verbose=args.verbose)

    # Print banner unless suppressed
    if not args.no_banner:
        aggregator.print_banner()

    # Route to appropriate scanner based on input type
    try:
        if args.username:
            if not validate_username(args.username):
                print(f"{Colors.FAIL}❌ Invalid username format{Colors.ENDC}")
                sys.exit(1)
            aggregator.scan_username(args.username, args.platforms)

        elif args.email:
            if not validate_email(args.email):
                print(f"{Colors.FAIL}❌ Invalid email format{Colors.ENDC}")
                sys.exit(1)
            aggregator.scan_email(args.email)

        elif args.ip:
            if not validate_ip(args.ip):
                print(f"{Colors.FAIL}❌ Invalid IP address format{Colors.ENDC}")
                sys.exit(1)
            aggregator.scan_ip(args.ip)

        # Export results if requested
        if args.export:
            aggregator.export_results(args.export, args.output)

        print(f"\n{Colors.GREEN}✅ Scan completed successfully!{Colors.ENDC}\n")

    except KeyboardInterrupt:
        print(f"\n\n{Colors.WARNING}⚠️  Scan interrupted by user{Colors.ENDC}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{Colors.FAIL}❌ Fatal error: {str(e)}{Colors.ENDC}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
